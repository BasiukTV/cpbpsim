import os

max_block_id = 0
unique_block_count = 0

rel_forks_count = 0
rel_forks = {}

for file_name in list(sorted(os.listdir("/media/pg_data_ssd/6hour_tpcc_pg_logs/"))):
    if not os.path.isfile("/media/pg_data_ssd/6hour_tpcc_pg_logs/{}".format(file_name)):
        continue

    print("Processing file: {}".format(file_name))

    with open("/media/pg_data_ssd/6hour_tpcc_pg_logs/{}".format(file_name)) as file:

        file_size = os.path.getsize("/media/pg_data_ssd/6hour_tpcc_pg_logs/{}".format(file_name))
        records_counter = 0

        log_line = file.readline().strip()
        while log_line:
            log_line = log_line.split(',')
            if len(log_line) == 5:
                timestamp, user, rel_fork, block_id, typ = log_line

                if user[:9] == "tpcc_user":
                    block_id = int(block_id)
                    if block_id > max_block_id:
                        max_block_id = block_id

                    if rel_fork not in rel_forks:
                        rel_forks_count += 1
                        rel_forks[rel_fork] = set()

                    if block_id not in rel_forks[rel_fork]:
                        rel_forks[rel_fork].add(block_id)
                        unique_block_count += 1

            records_counter += 1
            if records_counter == 10000:
                records_counter = 0
                print("\rProgress: {:6.2f}%".format(100 * file.tell() / file_size), end='')

            log_line = file.readline().strip()
    print("Progress: 100%")

print("Max Block ID: {}".format(max_block_id))
print("Unique Block Count: {}".format(unique_block_count))
print("Unique Rel Forks Count: {}".format(rel_forks_count))
