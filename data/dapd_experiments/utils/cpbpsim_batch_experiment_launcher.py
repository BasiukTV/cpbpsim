import logging, threading, time, subprocess

def thread_function(name, cli_arguments):
    logging.info("Thread %s: starting", name)
    logging.info("Running: %s", cli_arguments)
    subprocess.run(cli_arguments, shell=True, check=True)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    jobs = [
        """
        [
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_1x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/baseline/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/baseline/logs/tpcc_1x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/baseline/results/tpcc_1x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_2x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/baseline/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/baseline/logs/tpcc_2x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/baseline/results/tpcc_2x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_4x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/baseline/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/baseline/logs/tpcc_4x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/baseline/results/tpcc_4x_latency.csv"
        ],
        [
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_8x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/baseline/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/baseline/logs/tpcc_8x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/baseline/results/tpcc_8x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_16x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/baseline/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/baseline/logs/tpcc_16x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/baseline/results/tpcc_16x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_1x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/2lru/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru/logs/tpcc_1x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru/results/tpcc_1x_latency.csv"
        ],
        [
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_2x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/2lru/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru/logs/tpcc_2x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru/results/tpcc_2x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_4x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/2lru/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru/logs/tpcc_4x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru/results/tpcc_4x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_8x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/2lru/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru/logs/tpcc_8x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru/results/tpcc_8x_latency.csv"
        ],
        [
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_16x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/2lru/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru/logs/tpcc_16x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru/results/tpcc_16x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_1x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q/logs/tpcc_1x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q/results/tpcc_1x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_2x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q/logs/tpcc_2x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q/results/tpcc_2x_latency.csv"
        ],
        [
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_4x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q/logs/tpcc_4x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q/results/tpcc_4x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_8x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q/logs/tpcc_8x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q/results/tpcc_8x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_16x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q/logs/tpcc_16x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q/results/tpcc_16x_latency.csv"
        ],
        [
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_1x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_1x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_1x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_2x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_2x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_2x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_4x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_4x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_4x_latency.csv"
        ],
        [
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_8x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_8x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_8x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_16x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_16x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_16x_latency.csv"
        ],
        """
        [
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_025x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/baseline/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/baseline/logs/tpcc_025x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/baseline/results/tpcc_025x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_05x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/baseline/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/baseline/logs/tpcc_05x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/baseline/results/tpcc_05x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_025x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/2lru/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru/logs/tpcc_025x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru/results/tpcc_025x_latency.csv"
        ],
        [
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_05x_latency_tier_params.csv --tier-daps data/dapd_experiments/baseline/tier_daps.csv --tier-deps data/dapd_experiments/2lru/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru/logs/tpcc_05x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru/results/tpcc_05x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_025x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q/logs/tpcc_025x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q/results/tpcc_025x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_05x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q/logs/tpcc_05x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q/results/tpcc_05x_latency.csv"
        ],
        [
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_025x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_025x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_025x_latency.csv",
            "python3 cpbpsim/bp_simulator.py --workers 100 --tier-params data/dapd_experiments/tpcc_05x_latency_tier_params.csv --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv --byte-addressability data/dapd_experiments/byte_addressability.csv --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_05x_latency.log --log-level INFO --warmup 60000 --to-time 600000 --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_05x_latency.csv"
        ]
    ]

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