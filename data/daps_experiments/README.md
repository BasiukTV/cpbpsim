## DAPD 2020 Experiments Notebook

### Baseline

#### 05x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/daps_experiments/tpcc_05x_latency_tier_params.csv \
    --tier-daps data/daps_experiments/baseline/tier_daps.csv \
    --tier-deps data/daps_experiments/baseline/tier_deps.csv \
    --tenant-slas data/daps_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/daps_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/daps_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/3hr_12st_16ten_v3_pas.csv \
    --log-file data/daps_experiments/baseline/logs/tpcc_05x_latency.log \
    --log-level INFO \
    --warmup 900000 \
    --output-file data/daps_experiments/baseline/results/tpcc_05x_latency.csv </dev/null &>/dev/null &
```

#### 1x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/daps_experiments/tpcc_1x_latency_tier_params.csv \
    --tier-daps data/daps_experiments/baseline/tier_daps.csv \
    --tier-deps data/daps_experiments/baseline/tier_deps.csv \
    --tenant-slas data/daps_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/daps_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/daps_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/3hr_12st_16ten_v3_pas.csv \
    --log-file data/daps_experiments/baseline/logs/tpcc_1x_latency.log \
    --log-level INFO \
    --warmup 900000 \
    --output-file data/daps_experiments/baseline/results/tpcc_1x_latency.csv </dev/null &>/dev/null &
```

#### 2x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/daps_experiments/tpcc_2x_latency_tier_params.csv \
    --tier-daps data/daps_experiments/baseline/tier_daps.csv \
    --tier-deps data/daps_experiments/baseline/tier_deps.csv \
    --tenant-slas data/daps_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/daps_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/daps_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/3hr_12st_16ten_v3_pas.csv \
    --log-file data/daps_experiments/baseline/logs/tpcc_2x_latency.log \
    --log-level INFO \
    --warmup 900000 \
    --output-file data/daps_experiments/baseline/results/tpcc_2x_latency.csv </dev/null &>/dev/null &
```

#### 4x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/daps_experiments/tpcc_4x_latency_tier_params.csv \
    --tier-daps data/daps_experiments/baseline/tier_daps.csv \
    --tier-deps data/daps_experiments/baseline/tier_deps.csv \
    --tenant-slas data/daps_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/daps_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/daps_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/3hr_12st_16ten_v3_pas.csv \
    --log-file data/daps_experiments/baseline/logs/tpcc_4x_latency.log \
    --log-level INFO \
    --warmup 900000 \
    --output-file data/daps_experiments/baseline/results/tpcc_4x_latency.csv </dev/null &>/dev/null &
```

### 2LRU

#### 1x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/daps_experiments/tpcc_1x_latency_tier_params.csv \
    --tier-daps data/daps_experiments/baseline/tier_daps.csv \
    --tier-deps data/daps_experiments/2lru/tier_deps.csv \
    --tenant-slas data/daps_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/daps_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/daps_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/3hr_12st_16ten_v3_pas.csv \
    --log-file data/daps_experiments/2lru/logs/tpcc_1x_latency.log \
    --log-level INFO \
    --warmup 900000 \
    --output-file data/daps_experiments/2lru/results/tpcc_1x_latency.csv </dev/null &>/dev/null &
```