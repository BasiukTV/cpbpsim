## DAPD 2020 Experiments Notebook

### Baseline

#### Initialize From Files and Dump State to a Directory
```
$ time python3 cpbpsim/bp_simulator.py \
    --workers 5 \
    --tier-params data/daps_experiments/tier_params.csv \
    --tier-daps data/daps_experiments/baseline/tier_daps.csv \
    --tier-deps data/daps_experiments/baseline/tier_deps.csv \
    --tenant-slas data/daps_experiments/tenant_slas.csv \
    --tenant-dmps data/daps_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/daps_experiments/byte_addressability.csv \
    --pas-file data/page_access_sequence.csv \
    --log-file data/daps_experiments/baseline/logs/run1.log \
    --log-level INFO \
    --sim-state-dump-dir data/daps_experiments/baseline/dump_dir/ \
    --output-file data/daps_experiments/baseline/results/result1.csv
```

#### Initialize From Dump State
```
$ time python3 cpbpsim/bp_simulator.py \
    --init-dir data/daps_experiments/baseline/dump_dir/ \
    --pas-file data/page_access_sequence.csv \
    --log-file data/daps_experiments/baseline/logs/run2.log \
    --log-level INFO \
    --output-file data/daps_experiments/baseline/results/result2.csv
```