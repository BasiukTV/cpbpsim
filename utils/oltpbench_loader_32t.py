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
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_gold_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t4_gold_burst.xml --create=true --load=true"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_silver_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_silver_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_silver_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t12_silver_burst.xml --create=true --load=true"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t14_bronze_flat.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t15_bronze_burst.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t16_bronze_burst.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t23_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t24_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t25_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t26_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t27_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t28_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t29_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t30_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t31_bronze_100.xml --create=true --load=true",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t32_bronze_100.xml --create=true --load=true"
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
