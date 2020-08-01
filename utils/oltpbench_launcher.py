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
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_40.xml --execute=true -s 10 -o t2_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_40.xml --execute=true -s 10 -o t3_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t4_burst_400.xml --execute=true -s 10 -o t4_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_40.xml --execute=true -s 10 -o t6_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_40.xml --execute=true -s 10 -o t7_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_burst_400.xml --execute=true -s 10 -o t8_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_40.xml --execute=true -s 10 -o t10_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_40.xml --execute=true -s 10 -o t11_1_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t12_burst_400.xml --execute=true -s 10 -o t12_1_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_60.xml --execute=true -s 10 -o t2_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_60.xml --execute=true -s 10 -o t3_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t4_burst_400.xml --execute=true -s 10 -o t4_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_60.xml --execute=true -s 10 -o t6_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_60.xml --execute=true -s 10 -o t7_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_burst_400.xml --execute=true -s 10 -o t8_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_60.xml --execute=true -s 10 -o t10_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_60.xml --execute=true -s 10 -o t11_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t12_burst_400.xml --execute=true -s 10 -o t12_2_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_80.xml --execute=true -s 10 -o t2_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_80.xml --execute=true -s 10 -o t3_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_80.xml --execute=true -s 10 -o t6_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_80.xml --execute=true -s 10 -o t7_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_80.xml --execute=true -s 10 -o t10_3_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_80.xml --execute=true -s 10 -o t11_3_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_100.xml --execute=true -s 10 -o t2_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_100.xml --execute=true -s 10 -o t3_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_100.xml --execute=true -s 10 -o t6_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_100.xml --execute=true -s 10 -o t7_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_100.xml --execute=true -s 10 -o t10_4_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_100.xml --execute=true -s 10 -o t11_4_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_120.xml --execute=true -s 10 -o t2_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_120.xml --execute=true -s 10 -o t3_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_120.xml --execute=true -s 10 -o t6_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_120.xml --execute=true -s 10 -o t7_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_120.xml --execute=true -s 10 -o t10_5_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_120.xml --execute=true -s 10 -o t11_5_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_140.xml --execute=true -s 10 -o t2_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_140.xml --execute=true -s 10 -o t3_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_140.xml --execute=true -s 10 -o t6_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_140.xml --execute=true -s 10 -o t7_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_140.xml --execute=true -s 10 -o t10_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_140.xml --execute=true -s 10 -o t11_6_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_160.xml --execute=true -s 10 -o t2_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_160.xml --execute=true -s 10 -o t3_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_160.xml --execute=true -s 10 -o t6_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_160.xml --execute=true -s 10 -o t7_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_160.xml --execute=true -s 10 -o t10_7_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_160.xml --execute=true -s 10 -o t11_7_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_140.xml --execute=true -s 10 -o t2_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_140.xml --execute=true -s 10 -o t3_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_140.xml --execute=true -s 10 -o t6_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_140.xml --execute=true -s 10 -o t7_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_140.xml --execute=true -s 10 -o t10_8_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_140.xml --execute=true -s 10 -o t11_8_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_120.xml --execute=true -s 10 -o t2_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_120.xml --execute=true -s 10 -o t3_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_120.xml --execute=true -s 10 -o t6_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_120.xml --execute=true -s 10 -o t7_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_120.xml --execute=true -s 10 -o t10_9_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_120.xml --execute=true -s 10 -o t11_9_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_100.xml --execute=true -s 10 -o t2_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_100.xml --execute=true -s 10 -o t3_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_100.xml --execute=true -s 10 -o t6_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_100.xml --execute=true -s 10 -o t7_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_100.xml --execute=true -s 10 -o t10_10_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_100.xml --execute=true -s 10 -o t11_10_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_80.xml --execute=true -s 10 -o t2_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_80.xml --execute=true -s 10 -o t3_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_80.xml --execute=true -s 10 -o t6_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_80.xml --execute=true -s 10 -o t7_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_80.xml --execute=true -s 10 -o t10_11_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_80.xml --execute=true -s 10 -o t11_11_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_60.xml --execute=true -s 10 -o t2_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_60.xml --execute=true -s 10 -o t3_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t4_burst_400.xml --execute=true -s 10 -o t4_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_60.xml --execute=true -s 10 -o t6_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_60.xml --execute=true -s 10 -o t7_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_burst_400.xml --execute=true -s 10 -o t8_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_60.xml --execute=true -s 10 -o t10_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_60.xml --execute=true -s 10 -o t11_12_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t12_burst_400.xml --execute=true -s 10 -o t12_12_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_40.xml --execute=true -s 10 -o t2_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_40.xml --execute=true -s 10 -o t3_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t4_burst_400.xml --execute=true -s 10 -o t4_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_40.xml --execute=true -s 10 -o t6_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_40.xml --execute=true -s 10 -o t7_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_burst_400.xml --execute=true -s 10 -o t8_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_40.xml --execute=true -s 10 -o t10_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_40.xml --execute=true -s 10 -o t11_13_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t12_burst_400.xml --execute=true -s 10 -o t12_13_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_60.xml --execute=true -s 10 -o t2_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_60.xml --execute=true -s 10 -o t3_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t4_burst_400.xml --execute=true -s 10 -o t4_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_60.xml --execute=true -s 10 -o t6_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_60.xml --execute=true -s 10 -o t7_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_burst_400.xml --execute=true -s 10 -o t8_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_60.xml --execute=true -s 10 -o t10_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_60.xml --execute=true -s 10 -o t11_14_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t12_burst_400.xml --execute=true -s 10 -o t12_14_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_15_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_80.xml --execute=true -s 10 -o t2_15_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_80.xml --execute=true -s 10 -o t3_15_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_15_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_80.xml --execute=true -s 10 -o t6_15_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_80.xml --execute=true -s 10 -o t7_15_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_15_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_80.xml --execute=true -s 10 -o t10_15_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_80.xml --execute=true -s 10 -o t11_15_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_16_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_100.xml --execute=true -s 10 -o t2_16_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_100.xml --execute=true -s 10 -o t3_16_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_16_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_100.xml --execute=true -s 10 -o t6_16_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_100.xml --execute=true -s 10 -o t7_16_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_16_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_100.xml --execute=true -s 10 -o t10_16_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_100.xml --execute=true -s 10 -o t11_16_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_17_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_120.xml --execute=true -s 10 -o t2_17_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_120.xml --execute=true -s 10 -o t3_17_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_17_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_120.xml --execute=true -s 10 -o t6_17_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_120.xml --execute=true -s 10 -o t7_17_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_17_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_120.xml --execute=true -s 10 -o t10_17_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_120.xml --execute=true -s 10 -o t11_17_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_18_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_140.xml --execute=true -s 10 -o t2_18_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_140.xml --execute=true -s 10 -o t3_18_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_18_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_140.xml --execute=true -s 10 -o t6_18_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_140.xml --execute=true -s 10 -o t7_18_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_18_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_140.xml --execute=true -s 10 -o t10_18_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_140.xml --execute=true -s 10 -o t11_18_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_19_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_160.xml --execute=true -s 10 -o t2_19_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_160.xml --execute=true -s 10 -o t3_19_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_19_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_160.xml --execute=true -s 10 -o t6_19_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_160.xml --execute=true -s 10 -o t7_19_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_6_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_160.xml --execute=true -s 10 -o t10_19_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_160.xml --execute=true -s 10 -o t11_19_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_20_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_140.xml --execute=true -s 10 -o t2_20_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_140.xml --execute=true -s 10 -o t3_20_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_20_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_140.xml --execute=true -s 10 -o t6_20_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_140.xml --execute=true -s 10 -o t7_20_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_20_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_140.xml --execute=true -s 10 -o t10_20_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_140.xml --execute=true -s 10 -o t11_20_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_21_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_120.xml --execute=true -s 10 -o t2_21_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_120.xml --execute=true -s 10 -o t3_21_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_21_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_120.xml --execute=true -s 10 -o t6_21_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_120.xml --execute=true -s 10 -o t7_21_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_21_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_120.xml --execute=true -s 10 -o t10_21_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_120.xml --execute=true -s 10 -o t11_21_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_22_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_100.xml --execute=true -s 10 -o t2_22_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_100.xml --execute=true -s 10 -o t3_22_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_22_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_100.xml --execute=true -s 10 -o t6_22_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_100.xml --execute=true -s 10 -o t7_22_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_22_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_100.xml --execute=true -s 10 -o t10_22_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_100.xml --execute=true -s 10 -o t11_22_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_23_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_80.xml --execute=true -s 10 -o t2_23_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_80.xml --execute=true -s 10 -o t3_23_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_23_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_80.xml --execute=true -s 10 -o t6_23_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_80.xml --execute=true -s 10 -o t7_23_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_23_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_80.xml --execute=true -s 10 -o t10_23_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_80.xml --execute=true -s 10 -o t11_23_result"
        ],
        [
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o t1_24_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t2_period_60.xml --execute=true -s 10 -o t2_24_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t3_period_60.xml --execute=true -s 10 -o t3_24_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t4_burst_400.xml --execute=true -s 10 -o t4_24_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t5_flat.xml --execute=true -s 10 -o t5_2_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t6_period_60.xml --execute=true -s 10 -o t6_24_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t7_period_60.xml --execute=true -s 10 -o t7_24_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t8_burst_400.xml --execute=true -s 10 -o t8_24_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t9_flat.xml --execute=true -s 10 -o t9_24_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t10_period_60.xml --execute=true -s 10 -o t10_24_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t11_period_60.xml --execute=true -s 10 -o t11_24_result",
            "./oltpbenchmark -b tpcc -c cpbptun_experiments/t12_burst_400.xml --execute=true -s 10 -o t12_24_result"
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
