## About
This tool simulates the operation of a DBMS buffer pool manager which supports:
- Multi-tenancy with SLA violation penalty functions
- Multi-tier storage architecture (SSD-NVM-RAM is the intention).

INPUT:
- Input file with page access sequence.
- Input file with the storage tier parameters.
- Input file with the tier data admission policies.
- Input file with the tier data eviction policies.
- Input file with tenant SLA parameters.
- Input file with tenant data migration policies.
- Warmup time in ms.
- Logging level.
- Log file. Default.

OUTPUT:
- SLA violation penalty accrued by each tenant.

## Usage Help
```
$ python3 bp_simulator.py -h
```

## Usage Examples
[HardBD & Active 2020 Experiment](data_sets/harddb_active_experiments/)
