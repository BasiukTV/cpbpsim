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
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_40.xml --execute=true -s 10 -o t2_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t4_gold_burst.xml --execute=true -s 10 -o t4_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_40.xml --execute=true -s 10 -o t6_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_40.xml --execute=true -s 10 -o t7_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_40.xml --execute=true -s 10 -o t8_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t12_silver_burst.xml --execute=true -s 10 -o t12_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_40.xml --execute=true -s 10 -o t17_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_40.xml --execute=true -s 10 -o t18_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_40.xml --execute=true -s 10 -o t19_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_40.xml --execute=true -s 10 -o t20_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_40.xml --execute=true -s 10 -o t21_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_40.xml --execute=true -s 10 -o t22_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t15_bronze_burst.xml --execute=true -s 10 -o t15_1_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_60.xml --execute=true -s 10 -o t2_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t4_gold_burst.xml --execute=true -s 10 -o t4_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_60.xml --execute=true -s 10 -o t6_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_60.xml --execute=true -s 10 -o t7_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_60.xml --execute=true -s 10 -o t8_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t12_silver_burst.xml --execute=true -s 10 -o t12_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_60.xml --execute=true -s 10 -o t17_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_60.xml --execute=true -s 10 -o t18_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_60.xml --execute=true -s 10 -o t19_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_60.xml --execute=true -s 10 -o t20_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_60.xml --execute=true -s 10 -o t21_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_60.xml --execute=true -s 10 -o t22_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t15_bronze_burst.xml --execute=true -s 10 -o t15_2_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_80.xml --execute=true -s 10 -o t2_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_80.xml --execute=true -s 10 -o t6_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_80.xml --execute=true -s 10 -o t7_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_80.xml --execute=true -s 10 -o t8_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_80.xml --execute=true -s 10 -o t17_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_80.xml --execute=true -s 10 -o t18_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_80.xml --execute=true -s 10 -o t19_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_80.xml --execute=true -s 10 -o t20_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_80.xml --execute=true -s 10 -o t21_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_80.xml --execute=true -s 10 -o t22_3_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_100.xml --execute=true -s 10 -o t2_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_100.xml --execute=true -s 10 -o t6_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_100.xml --execute=true -s 10 -o t7_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_100.xml --execute=true -s 10 -o t8_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_100.xml --execute=true -s 10 -o t17_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_100.xml --execute=true -s 10 -o t18_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_100.xml --execute=true -s 10 -o t19_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_100.xml --execute=true -s 10 -o t20_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_100.xml --execute=true -s 10 -o t21_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_100.xml --execute=true -s 10 -o t22_4_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_120.xml --execute=true -s 10 -o t2_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_120.xml --execute=true -s 10 -o t6_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_120.xml --execute=true -s 10 -o t7_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_120.xml --execute=true -s 10 -o t8_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_120.xml --execute=true -s 10 -o t17_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_120.xml --execute=true -s 10 -o t18_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_120.xml --execute=true -s 10 -o t19_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_120.xml --execute=true -s 10 -o t20_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_120.xml --execute=true -s 10 -o t21_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_120.xml --execute=true -s 10 -o t22_5_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_140.xml --execute=true -s 10 -o t2_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_140.xml --execute=true -s 10 -o t6_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_140.xml --execute=true -s 10 -o t7_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_140.xml --execute=true -s 10 -o t8_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_140.xml --execute=true -s 10 -o t17_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_140.xml --execute=true -s 10 -o t18_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_140.xml --execute=true -s 10 -o t19_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_140.xml --execute=true -s 10 -o t20_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_140.xml --execute=true -s 10 -o t21_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_140.xml --execute=true -s 10 -o t22_6_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_160.xml --execute=true -s 10 -o t2_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_160.xml --execute=true -s 10 -o t6_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_160.xml --execute=true -s 10 -o t7_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_160.xml --execute=true -s 10 -o t8_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_160.xml --execute=true -s 10 -o t17_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_160.xml --execute=true -s 10 -o t18_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_160.xml --execute=true -s 10 -o t19_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_160.xml --execute=true -s 10 -o t20_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_160.xml --execute=true -s 10 -o t21_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_160.xml --execute=true -s 10 -o t22_7_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_140.xml --execute=true -s 10 -o t2_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_140.xml --execute=true -s 10 -o t6_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_140.xml --execute=true -s 10 -o t7_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_140.xml --execute=true -s 10 -o t8_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_140.xml --execute=true -s 10 -o t17_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_140.xml --execute=true -s 10 -o t18_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_140.xml --execute=true -s 10 -o t19_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_140.xml --execute=true -s 10 -o t20_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_140.xml --execute=true -s 10 -o t21_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_140.xml --execute=true -s 10 -o t22_8_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_120.xml --execute=true -s 10 -o t2_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_120.xml --execute=true -s 10 -o t6_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_120.xml --execute=true -s 10 -o t7_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_120.xml --execute=true -s 10 -o t8_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_120.xml --execute=true -s 10 -o t17_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_120.xml --execute=true -s 10 -o t18_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_120.xml --execute=true -s 10 -o t19_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_120.xml --execute=true -s 10 -o t20_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_120.xml --execute=true -s 10 -o t21_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_120.xml --execute=true -s 10 -o t22_9_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_100.xml --execute=true -s 10 -o t2_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_100.xml --execute=true -s 10 -o t6_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_100.xml --execute=true -s 10 -o t7_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_100.xml --execute=true -s 10 -o t8_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_100.xml --execute=true -s 10 -o t17_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_100.xml --execute=true -s 10 -o t18_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_100.xml --execute=true -s 10 -o t19_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_100.xml --execute=true -s 10 -o t20_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_100.xml --execute=true -s 10 -o t21_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_100.xml --execute=true -s 10 -o t22_10_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_80.xml --execute=true -s 10 -o t2_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_80.xml --execute=true -s 10 -o t6_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_80.xml --execute=true -s 10 -o t7_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_80.xml --execute=true -s 10 -o t8_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_80.xml --execute=true -s 10 -o t17_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_80.xml --execute=true -s 10 -o t18_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_80.xml --execute=true -s 10 -o t19_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_80.xml --execute=true -s 10 -o t20_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_80.xml --execute=true -s 10 -o t21_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_80.xml --execute=true -s 10 -o t22_11_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_gold_flat.xml --execute=true -s 10 -o t1_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_gold_60.xml --execute=true -s 10 -o t2_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t4_gold_burst.xml --execute=true -s 10 -o t4_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_silver_flat.xml --execute=true -s 10 -o t5_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_silver_60.xml --execute=true -s 10 -o t6_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_silver_60.xml --execute=true -s 10 -o t7_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_silver_60.xml --execute=true -s 10 -o t8_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t12_silver_burst.xml --execute=true -s 10 -o t12_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t13_bronze_flat.xml --execute=true -s 10 -o t13_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t17_bronze_60.xml --execute=true -s 10 -o t17_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t18_bronze_60.xml --execute=true -s 10 -o t18_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t19_bronze_60.xml --execute=true -s 10 -o t19_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t20_bronze_60.xml --execute=true -s 10 -o t20_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t21_bronze_60.xml --execute=true -s 10 -o t21_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t22_bronze_60.xml --execute=true -s 10 -o t22_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t15_bronze_burst.xml --execute=true -s 10 -o t15_12_result"
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
