# DAPD 2020 Experiments Notebook

## Latency Experiments

### Baseline

#### 025x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_025x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_025x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_025x_latency.csv </dev/null &>/dev/null &
```

#### 05x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_05x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_05x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_05x_latency.csv </dev/null &>/dev/null &
```

#### 1x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_1x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_1x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_1x_latency.csv </dev/null &>/dev/null &
```

#### 2x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_2x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_2x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_2x_latency.csv </dev/null &>/dev/null &
```

#### 4x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_4x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_4x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_4x_latency.csv </dev/null &>/dev/null &
```

#### 8x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_8x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_8x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_8x_latency.csv </dev/null &>/dev/null &
```

#### 16x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_16x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_16x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_16x_latency.csv </dev/null &>/dev/null &
```

### 2LRU

#### 025x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_025x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_025x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_025x_latency.csv </dev/null &>/dev/null &
```

#### 05x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_05x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_05x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_05x_latency.csv </dev/null &>/dev/null &
```

#### 1x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_1x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_1x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_1x_latency.csv </dev/null &>/dev/null &
```

#### 2x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_2x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_2x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_2x_latency.csv </dev/null &>/dev/null &
```

#### 4x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_4x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_4x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_4x_latency.csv </dev/null &>/dev/null &
```

#### 8x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_8x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_8x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_8x_latency.csv </dev/null &>/dev/null &
```

#### 16x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_16x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_16x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_16x_latency.csv </dev/null &>/dev/null &
```

### 2LRU-2Q

#### 025x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_025x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_025x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_025x_latency.csv </dev/null &>/dev/null &
```

#### 05x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_05x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_05x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_05x_latency.csv </dev/null &>/dev/null &
```

#### 1x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_1x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_1x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_1x_latency.csv </dev/null &>/dev/null &
```

#### 2x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_2x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_2x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_2x_latency.csv </dev/null &>/dev/null &
```

#### 4x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_4x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_4x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_4x_latency.csv </dev/null &>/dev/null &
```

#### 8x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_8x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_8x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_8x_latency.csv </dev/null &>/dev/null &
```

#### 16x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_16x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_16x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_16x_latency.csv </dev/null &>/dev/null &
```

### 2LRU-2Q-HDMP

#### 025x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_025x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_025x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_025x_latency.csv </dev/null &>/dev/null &
```

#### 05x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_05x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_05x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_05x_latency.csv </dev/null &>/dev/null &
```

#### 1x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_1x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_1x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_1x_latency.csv </dev/null &>/dev/null &
```

#### 2x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_2x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_2x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_2x_latency.csv </dev/null &>/dev/null &
```

#### 4x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_4x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_4x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_4x_latency.csv </dev/null &>/dev/null &
```

#### 8x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_8x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_8x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_8x_latency.csv </dev/null &>/dev/null &
```

#### 16x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_16x_latency_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_latency_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_16x_latency.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_16x_latency.csv </dev/null &>/dev/null &
```

## PMem Endurance Experiments

### Baseline

#### 025x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_025x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_025x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_025x_endurance.csv </dev/null &>/dev/null &
```

#### 05x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_05x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_05x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_05x_endurance.csv </dev/null &>/dev/null &
```

#### 1x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_1x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_1x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_1x_endurance.csv </dev/null &>/dev/null &
```

#### 2x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_2x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_2x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_2x_endurance.csv </dev/null &>/dev/null &
```

#### 4x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_4x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_4x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_4x_endurance.csv </dev/null &>/dev/null &
```

#### 8x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_8x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_8x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_8x_endurance.csv </dev/null &>/dev/null &
```

#### 16x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_16x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/baseline/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/baseline/logs/tpcc_16x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/baseline/results/tpcc_16x_endurance.csv </dev/null &>/dev/null &
```

### 2LRU

#### 025x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_025x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_025x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_025x_endurance.csv </dev/null &>/dev/null &
```

#### 05x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_05x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_05x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_05x_endurance.csv </dev/null &>/dev/null &
```

#### 1x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_1x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_1x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_1x_endurance.csv </dev/null &>/dev/null &
```

#### 2x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_2x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_2x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_2x_endurance.csv </dev/null &>/dev/null &
```

#### 4x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_4x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_4x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_4x_endurance.csv </dev/null &>/dev/null &
```

#### 8x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_8x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_8x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_8x_endurance.csv </dev/null &>/dev/null &
```

#### 16x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_16x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/baseline/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru/logs/tpcc_16x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru/results/tpcc_16x_endurance.csv </dev/null &>/dev/null &
```

### 2LRU-2Q

#### 025x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_025x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_025x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_025x_endurance.csv </dev/null &>/dev/null &
```

#### 05x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_05x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_05x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_05x_endurance.csv </dev/null &>/dev/null &
```

#### 1x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_1x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_1x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_1x_endurance.csv </dev/null &>/dev/null &
```

#### 2x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_2x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_2x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_2x_endurance.csv </dev/null &>/dev/null &
```

#### 4x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_4x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_4x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_4x_endurance.csv </dev/null &>/dev/null &
```

#### 8x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_8x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_8x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_8x_endurance.csv </dev/null &>/dev/null &
```

#### 16x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_16x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/baseline/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q/logs/tpcc_16x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q/results/tpcc_16x_endurance.csv </dev/null &>/dev/null &
```

### 2LRU-2Q-HDMP

#### 025x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_025x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_025x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_025x_endurance.csv </dev/null &>/dev/null &
```

#### 05x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_05x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_05x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_05x_endurance.csv </dev/null &>/dev/null &
```

#### 1x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_1x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_1x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_1x_endurance.csv </dev/null &>/dev/null &
```

#### 2x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_2x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_2x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_2x_endurance.csv </dev/null &>/dev/null &
```

#### 4x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_4x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_4x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_4x_endurance.csv </dev/null &>/dev/null &
```

#### 8x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_8x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_8x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_8x_endurance.csv </dev/null &>/dev/null &
```

#### 16x Resources
```
$ python3 cpbpsim/bp_simulator.py \
    --workers 100 \
    --tier-params data/dapd_experiments/tpcc_16x_endurance_tier_params.csv \
    --tier-daps data/dapd_experiments/2lru-2q-hdmp/tier_daps.csv \
    --tier-deps data/dapd_experiments/2lru-2q-hdmp/tier_deps.csv \
    --tenant-slas data/dapd_experiments/tpcc_tenant_endurance_slas.csv \
    --tenant-dmps data/dapd_experiments/2lru-2q-hdmp/tenant_dmps.csv \
    --byte-addressability data/dapd_experiments/byte_addressability.csv \
    --pas-file ../../tempfs/1hr_1st_16ten_v3_pas.csv \
    --log-file data/dapd_experiments/2lru-2q-hdmp/logs/tpcc_16x_endurance.log \
    --log-level INFO \
    --warmup 60000 \
    --to-time 600000 \
    --output-file data/dapd_experiments/2lru-2q-hdmp/results/tpcc_16x_endurance.csv </dev/null &>/dev/null &
```