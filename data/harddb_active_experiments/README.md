# HardBD&Active 2020 Experimentation Notebook

## Common Parameters

### Page Access Sequence Generation Parameters
```
$ time python3 cpbpsim/page_access_sequence_generator/page_access_sequence_generator.py \
    --output data/harddb_active_experiments/page_access_sequence.csv \
    --overwrite \
    --tenants 9 \
    --time 28800 \
    --access-rate 5 5 5 25 25 25 100 100 100 \
    --access-distribution UNI UNI UNI NOR_10 NOR_10 NOR_10 PAR_2 PAR_2 PAR_2 \
    --data-size 1000000 1000000 1000000 2000000 2000000 2000000 10000000 10000000 10000000 \
    --read-fraction 0.5 0.5 0.5 0.8 0.8 0.8 0.9 0.9 0.9
```

### Storage Tier Parameters
#### CSV file contents
```
name,free_space,CPU_access,type1,SLO1,cost1,type2,SLO2,cost2,type3,SLO3,cost3
SSD,100000000,FALSE,read,latency,25000,update,latency,300000,copy,latency,300000
NVM,2500000,TRUE,read,latency,100,update,latency,100,copy,latency,100
RAM,250000,TRUE,read,latency,50,update,latency,50,copy,latency,50
```

#### CSV file
[Storage Tier Parameters](tier_params.csv)

### Tenant SLAs
#### CSV file contents
```
tenantID,slo_type,eval_period,sla_func_type,param1,param2,param3,...
1,latency,10000,APWL,0.0,0.0,30000,0.0,0.01
2,latency,10000,APWL,0.0,0.0,30000,0.0,0.01
3,latency,10000,APWL,0.0,0.0,30000,0.0,0.01
4,latency,10000,APWL,0.0,0.0,30000,0.0,0.05
5,latency,10000,APWL,0.0,0.0,30000,0.0,0.05
6,latency,10000,APWL,0.0,0.0,30000,0.0,0.05
7,latency,10000,APWL,0.0,0.0,30000,0.0,0.2
8,latency,10000,APWL,0.0,0.0,30000,0.0,0.2
9,latency,10000,APWL,0.0,0.0,30000,0.0,0.2
```

#### CSV file
[Tenant SLAs](tenant_slas.csv)

## Baseline Experiment

### Baseline DEPs
```
tier_name,policy_name,policy_param1,policy_param2,policy_param3,...
SSD,FIFO
NVM,FIFO
RAM,FIFO
```

#### CSV file
[Baseline DEPs](baseline/tier_deps.csv)

### Baseline DAPs
```
tier_name,policy_name,policy_param1,policy_param2,policy_param3,...
SSD,EAG
NVM,EAG
RAM,NEV
```

#### CSV file
[Baseline DAPs](baseline/tier_daps.csv)

### Baseline DMPs
```
tenantID,type,tiers,tier1,tier2,...,param1,param2,param3,...
1,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
2,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
3,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
4,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
5,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
6,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
7,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
8,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
9,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
```

#### CSV file
[Baseline DMPs](baseline/tenant_dmps.csv)

### Simulator Execution Parameters
```
$ time python3 cpbpsim/bp_simulator.py \
    --tier-params data/harddb_active_experiments/tier_params.csv \
    --tier-daps data/harddb_active_experiments/baseline/tier_daps.csv \
    --tier-deps data/harddb_active_experiments/baseline/tier_deps.csv \
    --tenant-slas data/harddb_active_experiments/tenant_slas.csv \
    --tenant-dmps data/harddb_active_experiments/baseline/tenant_dmps.csv \
    --pas-file data/harddb_active_experiments/page_access_sequence.csv \
    --warmup 3600000 \
    --log-file data/harddb_active_experiments/baseline/logs/run1.log \
    --log-level INFO \
    > data/harddb_active_experiments/baseline/results/result1.csv
```

#### Simulation Results
* [Results](baseline/results/result1.csv)
* [Logs](baseline/logs/run1.log)

## LRU1 Experiment

### LRU1 DEPs
```
tier_name,policy_name,policy_param1,policy_param2,policy_param3,...
SSD,FIFO
NVM,FIFO
RAM,LRU
```

#### CSV file
[LRU1 DEPs](lru1/tier_deps.csv)

### Simulator Execution Parameters
```
$ time python3 cpbpsim/bp_simulator.py \
    --tier-params data/harddb_active_experiments/tier_params.csv \
    --tier-daps data/harddb_active_experiments/lru1/tier_daps.csv \
    --tier-deps data/harddb_active_experiments/lru1/tier_deps.csv \
    --tenant-slas data/harddb_active_experiments/tenant_slas.csv \
    --tenant-dmps data/harddb_active_experiments/lru1/tenant_dmps.csv \
    --warmup 3600000 \
    --pas-file data/harddb_active_experiments/page_access_sequence.csv \
    --log-file data/harddb_active_experiments/lru1/logs/run1.log \
    > data/harddb_active_experiments/lru1/results/result1.csv
```

#### Simulation Results
* [Results](lru1/results/result1.csv)
* [Logs](lru1/logs/run1.log)

## LRU2 Experiment

### LRU2 DEPs
```
tier_name,policy_name,policy_param1,policy_param2,policy_param3,...
SSD,FIFO
NVM,LRU
RAM,LRU
```

#### CSV file
[LRU2 DEPs](lru2/tier_deps.csv)

### Simulator Execution Parameters
```
$ time python3 cpbpsim/bp_simulator.py \
    --tier-params data/harddb_active_experiments/tier_params.csv \
    --tier-daps data/harddb_active_experiments/lru2/tier_daps.csv \
    --tier-deps data/harddb_active_experiments/lru2/tier_deps.csv \
    --tenant-slas data/harddb_active_experiments/tenant_slas.csv \
    --tenant-dmps data/harddb_active_experiments/lru2/tenant_dmps.csv \
    --pas-file data/harddb_active_experiments/page_access_sequence.csv \
    --warmup 3600000 \
    --log-file data/harddb_active_experiments/lru2/logs/run1.log \
    > data/harddb_active_experiments/lru2/results/result1.csv
```

#### Simulation Results
* [Results](lru2/results/result1.csv)
* [Logs](lru2/logs/run1.log)

## LRU2-2Q Experiment

### LRU2-2Q DAPs
```
tier_name,policy_name,policy_param1,policy_param2,policy_param3,...
SSD,EAG
NVM,2Q
RAM,NEV
```

#### CSV file
[LRU2-2Q DEPs](lru2-2q/tier_daps.csv)

### Simulator Execution Parameters
```
$ time python3 cpbpsim/bp_simulator.py \
    --tier-params data/harddb_active_experiments/tier_params.csv \
    --tier-daps data/harddb_active_experiments/lru2-2q/tier_daps.csv \
    --tier-deps data/harddb_active_experiments/lru2-2q/tier_deps.csv \
    --tenant-slas data/harddb_active_experiments/tenant_slas.csv \
    --tenant-dmps data/harddb_active_experiments/lru2-2q/tenant_dmps.csv \
    --pas-file data/harddb_active_experiments/page_access_sequence.csv \
    --warmup 3600000 \
    --log-file data/harddb_active_experiments/lru2-2q/logs/run1.log \
    > data/harddb_active_experiments/lru2-2q/results/result1.csv
```

#### Simulation Results
* [Results](lru2-2q/results/result1.csv)
* [Logs](lru2-2q/logs/run1.log)

## LRU2-2Q-HDMPS Experiment

### LRU2-2Q-HDMPS DMPs
```
tenantID,type,tiers,tier1,tier2,...,param1,param2,param3,...
1,PROB,3,SSD,NVM,RAM,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0
2,PROB,3,SSD,NVM,RAM,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0
3,PROB,3,SSD,NVM,RAM,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0
4,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
5,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
6,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
7,PROB,3,SSD,NVM,RAM,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0
8,PROB,3,SSD,NVM,RAM,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0
9,PROB,3,SSD,NVM,RAM,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0
```

#### CSV file
[LRU2-2Q-HDMPS DMPs](lru2-2q-hdmps/tenant_dmps.csv)

### Simulator Execution Parameters
```
$ time python3 cpbpsim/bp_simulator.py \
    --tier-params data/harddb_active_experiments/tier_params.csv \
    --tier-daps data/harddb_active_experiments/lru2-2q-hdmps/tier_daps.csv \
    --tier-deps data/harddb_active_experiments/lru2-2q-hdmps/tier_deps.csv \
    --tenant-slas data/harddb_active_experiments/tenant_slas.csv \
    --tenant-dmps data/harddb_active_experiments/lru2-2q-hdmps/tenant_dmps.csv \
    --pas-file data/harddb_active_experiments/page_access_sequence.csv \
    --warmup 3600000 \
    --log-file data/harddb_active_experiments/lru2-2q-hdmps/logs/run1.log \
    --log-level INFO \
    > data/harddb_active_experiments/lru2-2q-hdmps/results/result1.csv
```

#### Simulation Results
* [Results](lru2-2q-hdmps/results/result1.csv)
* [Logs](lru2-2q-hdmps/logs/run1.log)
