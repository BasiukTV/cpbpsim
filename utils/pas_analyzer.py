import os

# Containers for the counts across all evaluations
tot_access_count = {}
tot_read_count = {}
tot_unique_block_access_count = {}

# Containers for the counts per evaluation counts
eval_access_count = {}
eval_read_count = {}
eval_unique_block_access_count = {}

# How many blocks unused when all tenants service fraction of least popular requests
max_blocks_unused = {}
for i in range(1001):
    max_blocks_unused[float("{:5.3f}".format(i / 1000))] = 0

input_file_name = "../data/page_access_sequence.csv"
output_file_name = "analysis.txt"

#input_file_name = "../../PASs/3hr_12st_16ten_v3_pas.csv"
#output_file_name = "../data/daps_experiments/tpcc_3hr_12st_16ten_v3_pas_analysis.txt"

eval_period = 1
sla_eval_time = 30000 # 30 seconds in milliseconds
curr_eval_cutoff_time = sla_eval_time

with open(output_file_name, "w") as out:
    with open(input_file_name) as file:

        file_size = os.path.getsize(input_file_name)
        records_counter = 0

        file.readline() # Skip the header

        log_line = file.readline().strip()
        while log_line:
            log_line = log_line.split(',')

            timestamp, block_id, tenant_id, typ = log_line
            timestamp, block_id, tenant_id = int(timestamp), int(block_id), int(tenant_id)

            # For each SLA evaluation period, report per tenant access count and block footprint
            # Also, calculate per 
            if timestamp > curr_eval_cutoff_time:
                out.write("Analysis of Evaluation Period #{}\n".format(eval_period))

                tenants = eval_access_count.keys()
                blocks_unused = {}
                for i in range(1001):
                    blocks_unused[float("{:5.3f}".format(i / 1000))] = {}

                for t in tenants:
                    out.write("\tTenant {}:\n".format(t))

                    eval_accesses = eval_access_count[t]
                    out.write("\t\tTotal Accesses: {}, Read Ratio: {:6.2f}%\n".format(eval_accesses, (100 * eval_read_count[t]) / eval_accesses))

                    eval_blocks = len(eval_unique_block_access_count[t].keys())
                    out.write("\t\tTotal Unique Blocks: {}\n".format(eval_blocks))

                    accesses = 0
                    p = 0
                    per_block_access_counts = sorted(eval_unique_block_access_count[t].values())

                    for i in range(len(per_block_access_counts)):
                        accesses += per_block_access_counts[i]

                        while (accesses / eval_accesses) > p:
                            # Record how many blocks unused after least p percentage of accesses are covered
                            blocks_unused[float("{:5.3f}".format(p))][t] = int((1 - ((i + 1) / len(per_block_access_counts))) * eval_blocks)
                            p += 0.001

                    blocks_unused[1.0][t] = 0

                for p in blocks_unused:
                    total_blocks_unused = sum(blocks_unused[p].values())
                    if total_blocks_unused > max_blocks_unused[p]:
                        max_blocks_unused[p] = total_blocks_unused

                curr_eval_cutoff_time += sla_eval_time
                eval_period += 1
                eval_access_count = {}
                eval_read_count = {}
                eval_unique_block_access_count = {}

                print("\rProgress: {:6.2f}%".format(100 * file.tell() / file_size), end='')

            if tenant_id not in tot_access_count:
                tot_access_count[tenant_id] = 0
                tot_read_count[tenant_id] = 0
                tot_unique_block_access_count[tenant_id] = {}

            if tenant_id not in eval_access_count:
                eval_access_count[tenant_id] = 0
                eval_read_count[tenant_id] = 0
                eval_unique_block_access_count[tenant_id] = {}

            tot_access_count[tenant_id] = tot_access_count[tenant_id] + 1
            eval_access_count[tenant_id] = eval_access_count[tenant_id] + 1
            if typ == "read":
                tot_read_count[tenant_id] = tot_read_count[tenant_id] + 1
                eval_read_count[tenant_id] = eval_read_count[tenant_id] + 1

            if block_id not in tot_unique_block_access_count[tenant_id]:
                tot_unique_block_access_count[tenant_id][block_id] = 0

            if block_id not in eval_unique_block_access_count[tenant_id]:
                eval_unique_block_access_count[tenant_id][block_id] = 0

            tot_unique_block_access_count[tenant_id][block_id] = tot_unique_block_access_count[tenant_id][block_id] + 1
            eval_unique_block_access_count[tenant_id][block_id] = eval_unique_block_access_count[tenant_id][block_id] + 1

            log_line = file.readline().strip()

        print("\rProgress: 100.00%")

    out.write("Per Tenant Overall Analysis results:\n")
    tenants = list(sorted(tot_access_count.keys()))
    for t in tenants:
        out.write("\tTenant {}:\n".format(t))
        out.write("\t\tTotal Accesses: {}, Read Ratio: {:6.2f}%\n".format(tot_access_count[t], (100 * tot_read_count[t]) / tot_access_count[t]))

        tot_blocks = len(tot_unique_block_access_count[t].keys())
        out.write("\t\tTotal Unique Blocks: {}\n".format(tot_blocks))

        accesses = 0
        p = 0
        per_block_access_counts = sorted(tot_unique_block_access_count[t].values())

        out.write("\t\tTenant {} Cumulative Access Distribution:\n".format(t))
        out.write("\t\t\tratio_of_unique_least_popular_blocks,blocks_still_unused,ratio_of_least_popular_blocks_accesses\n")

        for i in range(len(per_block_access_counts)):
            accesses += per_block_access_counts[i]

            while (accesses / tot_access_count[t]) > p:
                out.write("{},{},{}\n".format(
                    float("{:5.3f}".format((i + 1) / len(per_block_access_counts))),
                    int((1 - ((i + 1) / len(per_block_access_counts))) * tot_blocks),
                    float("{:5.3f}".format(p))))
                p += 0.001

        out.write("1.0,0,1.0\n")

    out.write("Combined Free Pages Per Least Popular Page Accesses:\n")
    out.write("blocks_still_unused,ratio_of_least_popular_blocks_accesses\n")
    for p in sorted(max_blocks_unused.keys()):
        out.write("{},{}\n".format(max_blocks_unused[p], p))
