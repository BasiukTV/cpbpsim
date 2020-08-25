import os

rel_forks = {}
rel_fork_index = 0

access_count = {}
read_count = {}
unique_block_access_count = {}


for file_name in list(sorted(os.listdir("pgsql_logs/"))):
    if not os.path.isfile("pgsql_logs/{}".format(file_name)):
        continue

    print("Processing file: {}".format(file_name))

    with open("pgsql_logs/{}".format(file_name)) as file:

        file_size = os.path.getsize("pgsql_logs/{}".format(file_name))
        records_counter = 0

        log_line = file.readline().strip()
        while log_line:
            log_line = log_line.split(',')
            if len(log_line) == 5:
                timestamp, user, rel_fork, block_id, typ = log_line

                if user[:9] == "tpcc_user":

                    if rel_fork not in rel_forks:
                        rel_fork_index += 1
                        rel_forks[rel_fork] = rel_fork_index

                    tenant_id = int(user[9:])
                    if tenant_id not in access_count:
                        access_count[tenant_id] = 0
                        read_count[tenant_id] = 0
                        unique_block_access_count[tenant_id] = {}

                    access_count[tenant_id] = access_count[tenant_id] + 1
                    if typ == "read":
                        read_count[tenant_id] = read_count[tenant_id] + 1

                    block_id = (rel_forks[rel_fork] << 32) + int(block_id)

                    if block_id not in unique_block_access_count[tenant_id]:
                        unique_block_access_count[tenant_id][block_id] = 0

                    unique_block_access_count[tenant_id][block_id] = unique_block_access_count[tenant_id][block_id] + 1

            records_counter += 1
            if records_counter == 10000:
                records_counter = 0
                print("\rProgress: {:6.2f}%".format(100 * file.tell() / file_size), end='')

            log_line = file.readline().strip()
    print("\rProgress: 100.00%")

with open("analysis.txt", "w") as out:
    out.write("Analysis results:\n")
    tenants = list(sorted(access_count.keys()))
    for t in tenants:
        out.write("\tTenant {}:\n".format(t))
        out.write("\t\tTotal Accesses: {}, Read Ratio: {:6.2f}%\n".format(access_count[t], (100 * read_count[t]) / access_count[t]))

        tot_blocks = len(unique_block_access_count[t].keys())
        out.write("\t\tTotal Unique Blocks: {}\n".format(tot_blocks))

        accesses = 0
        p = 0
        per_block_access_counts = sorted(unique_block_access_count[t].values())
        cum_acc_distr = {}

        for i in range(len(per_block_access_counts)):
            accesses += per_block_access_counts[i]

            if i > p * len(per_block_access_counts):
                cum_acc_distr[float("{:5.3f}".format(p))] = float("{:8.6f}".format(accesses / access_count[t]))
                p += 0.001

        cum_acc_distr[1.0] = 1.0

        out.write("\t\tCumulative Access Distribution: {}\n".format(cum_acc_distr))
