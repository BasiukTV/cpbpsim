# PostgreSQL & TPC-C Experimentation Notebook

## Common Parameters

### Storage Tier Parameters

#### Explanation
* Assuming 32KB page size - 1GB worth of RAM, 10GB NVM, 2000GB of SSD.
* 6 Hour, 12 Tenant experiment referenced 802776 unique page IDs, which is approx 25.5GB of data footprint.

#### CSV file contents
```
name,free_space,CPU_access,type1,SLO1,cost1,type2,SLO2,cost2,type3,SLO3,cost3
SSD,65536000,False,read,latency,300000,update,latency,300000,copy,latency,300000
NVM,327680,True,read,latency,20,update,latency,50,copy,latency,50
RAM,32768,True,read,latency,10,update,latency,10,copy,latency,10
```

#### CSV file
[Storage Tier Parameters](simulator_init/tier_params.csv)

#### Alternative CSV file contents
```
name,free_space,CPU_access,type1,SLO1,cost1,type2,SLO2,cost2,type3,SLO3,cost3
SSD,65536000,False,read,latency,300000,update,latency,300000,copy,latency,300000
NVM,16384,True,read,latency,20,update,latency,50,copy,latency,50
RAM,16384,True,read,latency,10,update,latency,10,copy,latency,10
```

### Tenant SLAs

#### Explanation
* First four tenants - gold subscription, $0.2 per violation. Next four - silver, $0.06. Last four - bronze, $0.01.
* Each policy evaluated each 10 seconds for average page access latency.
* Threshold is the same for all tenants - 0.03ms, which roughly corresponds to over 10% of page accesses served from SSD.

#### CSV file contents
```
tenantID,slo_type,eval_period,sla_func_type,param1,param2,param3,...
1,latency,10000,APWL,0.0,0.0,30000,0.0,0.2
2,latency,10000,APWL,0.0,0.0,30000,0.0,0.2
3,latency,10000,APWL,0.0,0.0,30000,0.0,0.2
4,latency,10000,APWL,0.0,0.0,30000,0.0,0.2
5,latency,10000,APWL,0.0,0.0,30000,0.0,0.06
6,latency,10000,APWL,0.0,0.0,30000,0.0,0.06
7,latency,10000,APWL,0.0,0.0,30000,0.0,0.06
8,latency,10000,APWL,0.0,0.0,30000,0.0,0.06
9,latency,10000,APWL,0.0,0.0,30000,0.0,0.01
10,latency,10000,APWL,0.0,0.0,30000,0.0,0.01
11,latency,10000,APWL,0.0,0.0,30000,0.0,0.01
12,latency,10000,APWL,0.0,0.0,30000,0.0,0.01
```

#### CSV file
[Tenant SLAs](simulator_init/tenant_slas.csv)

### Storage Tier DEPs
```
tier_name,policy_name,policy_param1,policy_param2,policy_param3,...
SSD,NEV
NVM,LRU
RAM,LRU
```

#### CSV file
[Storage Tier DEPs](simulator_init/tier_deps.csv)

### Storage Tier DAPs
```
tier_name,policy_name,policy_param1,policy_param2,policy_param3,...
SSD,EAG
NVM,2Q
RAM,NEV
```

#### CSV file
[Storage Tier DAPs](simulator_init/tier_daps.csv)

### Tenant DMPs
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
10,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
11,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
12,PROB,3,SSD,NVM,RAM,0.0,0.5,0.5,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,0.0,0.0,0.5,0.5,0.0
```

#### CSV file
[Baseline DMPs](simulator_init/tenant_dmps.csv)

#### Explanation
* 6hours_12steps PAS file is 12.5 GB large, and we load it all in memory. So we only process 30 minutes of it below.

### Simulator Execution Parameters
```
$ time python3 cpbpsim/bp_simulator.py \
    --tier-params data/pg_tpcc_experiments/simulator_init/tier_params.csv \
    --tier-daps data/pg_tpcc_experiments/simulator_init/tier_daps.csv \
    --tier-deps data/pg_tpcc_experiments/simulator_init/tier_deps.csv \
    --tenant-slas data/pg_tpcc_experiments/simulator_init/tenant_slas.csv \
    --tenant-dmps data/pg_tpcc_experiments/simulator_init/tenant_dmps.csv \
    --pas-file ../6hours_12steps/pas.csv \
    --log-file ../6hours_12steps/cpbpsim/logs/run1.log \
    --log-level INFO \
    --output-file ../6hours_12steps/cpbpsim/results/result1.csv \
    --sim-state-dump-dir ../6hours_12steps/cpbpsim/state_dumps/ \
    --to-time 1800000
```

### Simulator Re-Start Parameters
```
$ time python3 cpbpsim/bp_simulator.py \
    --init-dir ../6hours_12steps/cpbpsim/state_dumps/ \
    --pas-file ../6hours_12steps/pas.csv \
    --log-file ../6hours_12steps/cpbpsim/logs/run1.log \
    --log-level INFO \
    --output-file ../6hours_12steps/cpbpsim/results/result1.csv \
    --sim-state-dump-dir ../6hours_12steps/cpbpsim/state_dumps/ \
    --from-time 180000 \
    --to-time 3600000
```

#### Simulation Results
* [Results](pg_tpcc_experiments_result.csv)
* [Logs](logs/run1.log)
