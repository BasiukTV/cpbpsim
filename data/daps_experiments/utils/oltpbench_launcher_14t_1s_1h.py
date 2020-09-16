import logging, threading, time, subprocess

def thread_function(name, cli_arguments):
    logging.info("Thread %s: starting", name)
    subprocess.run(cli_arguments, shell=True, check=True)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    jobs = [
        [
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t1_gold.xml --execute=true -s 10 -o t1_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t2_gold.xml --execute=true -s 10 -o t2_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t5_silver.xml --execute=true -s 10 -o t5_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t6_silver.xml --execute=true -s 10 -o t6_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t7_silver.xml --execute=true -s 10 -o t7_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t8_silver.xml --execute=true -s 10 -o t8_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t13_bronze.xml --execute=true -s 10 -o t13_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t14_bronze.xml --execute=true -s 10 -o t14_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t15_bronze.xml --execute=true -s 10 -o t15_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t16_bronze.xml --execute=true -s 10 -o t16_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t17_bronze.xml --execute=true -s 10 -o t17_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t18_bronze.xml --execute=true -s 10 -o t18_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t19_bronze.xml --execute=true -s 10 -o t19_result",
            "./oltpbenchmark -b tpcc -c tpcc_1hr_oltp_tenant_configs/t20_bronze.xml --execute=true -s 10 -o t20_result"
        ]]

    for bi in range(len(jobs)):
        threads = list()
        for ji in range(len(jobs[bi])):
            logging.info("Main    : create and start thread %d-%d", bi, ji)
            x = threading.Thread(target=thread_function, args=("{}-{}".format(bi, ji), jobs[bi][ji]))
            threads.append(x)
            x.start()

        for ji in range(len(threads)):
            logging.info("Main    : before joining thread %d-%d", bi, ji)
            threads[ji].join()
            logging.info("Main    : thread %d-%d done", bi, ji)
