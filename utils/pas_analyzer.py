import os

tot_access_count = {}
tot_read_count = {}
tot_unique_block_access_count = {}

input_file_name = ""
output_file_name = ""
sla_eval_time = 30000 # 30 seconds in milliseconds

with open(input_file_name) as file:

    file_size = os.path.getsize(input_file_name)
    records_counter = 0

    file.readline() # Skip the header

    log_line = file.readline().strip()
    while log_line:
        log_line = log_line.split(',')

        timestamp, block_id, tenant_id, typ = log_line

        if tenant_id not in tot_access_count:
            tot_access_count[tenant_id] = 0
            tot_read_count[tenant_id] = 0
            tot_unique_block_access_count[tenant_id] = {}

        tot_access_count[tenant_id] = tot_access_count[tenant_id] + 1
        if typ == "read":
            tot_read_count[tenant_id] = tot_read_count[tenant_id] + 1

        if block_id not in tot_unique_block_access_count[tenant_id]:
            tot_unique_block_access_count[tenant_id][block_id] = 0

        tot_unique_block_access_count[tenant_id][block_id] = tot_unique_block_access_count[tenant_id][block_id] + 1

        records_counter += 1
        if records_counter == 10000:
            records_counter = 0
            print("\rProgress: {:6.2f}%".format(100 * file.tell() / file_size), end='')

        log_line = file.readline().strip()

    print("\rProgress: 100.00%")

with open(output_file_name, "w") as out:
    out.write("Analysis results:\n")
    tenants = list(sorted(tot_access_count.keys()))
    for t in tenants:
        out.write("Tenant {}:\n".format(t))
        out.write("Total Accesses: {}, Read Ratio: {:6.2f}%\n".format(tot_access_count[t], (100 * tot_read_count[t]) / tot_access_count[t]))

        tot_blocks = len(tot_unique_block_access_count[t].keys())
        out.write("Total Unique Blocks: {}\n".format(tot_blocks))

        accesses = 0
        p = 0
        per_block_access_counts = sorted(tot_unique_block_access_count[t].values())
        cum_acc_distr = {}

        out.write("Tenant {} Cumulative Access Distribution:\n".format(t))

        for i in range(len(per_block_access_counts)):
            accesses += per_block_access_counts[i]

            if i > p * len(per_block_access_counts):
                out.write("{},{}\n".format(float("{:5.3f}".format(p)), float("{:8.6f}".format(accesses / tot_access_count[t]))))
                p += 0.001

        out.write("1.0,1.0\n")
