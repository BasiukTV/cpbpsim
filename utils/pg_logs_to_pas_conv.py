import os, datetime

rel_forks_count = 0
rel_forks = {}
timestamp_decrease = int(datetime.datetime.strptime(
    "2020-08-01 18:32:11.340 UTC"[:-4] + "000", '%Y-%m-%d %H:%M:%S.%f').timestamp() * 1000)

with open("4hour_24steps_pas.csv", 'w') as out_file:
    out_file.write("timestamp,pageID,tenantID,access_type\n")

    for file_name in list(sorted(os.listdir("/media/pg_data_ssd/4hour_24step_tpcc_pg_logs/"))):
        if not os.path.isfile("/media/pg_data_ssd/4hour_24step_tpcc_pg_logs/{}".format(file_name)):
            continue

        print("Processing file: {}".format(file_name))

        with open("/media/pg_data_ssd/4hour_24step_tpcc_pg_logs/{}".format(file_name)) as file:

            file_size = os.path.getsize("/media/pg_data_ssd/4hour_24step_tpcc_pg_logs/{}".format(file_name))
            records_counter = 0

            log_line = file.readline().strip()
            while log_line:
                log_line = log_line.split(',')
                if len(log_line) == 5:
                    timestamp, user, rel_fork, block_id, typ = log_line

                    if user[:9] == "tpcc_user":

                        timestamp = timestamp[:-4] + "000"
                        timestamp = int(datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f').timestamp() * 1000)
                        timestamp -= timestamp_decrease

                        user = user[9:]

                        block_id = int(block_id)
                        if rel_fork not in rel_forks:
                            rel_forks_count += 1
                            rel_forks[rel_fork] = rel_forks_count
                        block_id = (rel_forks[rel_fork] << 32) + block_id

                        out_file.write("{},{},{},{}\n".format(
                            timestamp, block_id, user, "read" if typ == "read" else "update"))

                records_counter += 1
                if records_counter == 1000:
                    records_counter = 0
                    print("\rProgress: {:6.2f}%".format(100 * file.tell() / file_size), end='')

                log_line = file.readline().strip()
        print("\rProgress: 100%")
