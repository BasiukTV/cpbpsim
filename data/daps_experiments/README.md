## DAPD 2020 Experiments Notebook

### Baseline

#### 1x Resources
```
$ time python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/daps_experiments/tpcc_1x_latency_tier_params.csv \
    --tier-daps data/daps_experiments/baseline/tier_daps.csv \
    --tier-deps data/daps_experiments/baseline/tier_deps.csv \
    --tenant-slas data/daps_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/daps_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/daps_experiments/byte_addressability.csv \
    --pas-file ../PASs/3hr_12st_16ten_v3_pas.csv \
    --log-file data/daps_experiments/baseline/logs/tpcc_1x_latency.log \
    --log-level INFO \
    --warmup 900000 \
    --output-file data/daps_experiments/baseline/results/tpcc_1x_latency.csv
```