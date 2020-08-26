## Usage Example

### Initialize From Files and Dump State to a Directory
```
$ time python3 cpbpsim/bp_simulator.py \
    --workers 5 \
    --tier-params data/tier_params.csv \
    --tier-daps data/tier_daps.csv \
    --tier-deps data/tier_deps.csv \
    --tenant-slas data/tenant_slas.csv \
    --tenant-dmps data/tenant_dmps.csv \
    --pas-file data/page_access_sequence.csv \
    --log-file data/logs/run1.log \
    --log-level INFO \
    --sim-state-dump-dir data/dump_dir/
```

### Initialize From Dump State
```
$ time python3 cpbpsim/bp_simulator.py \
    --init-dir data/dump_dir/ \
    --pas-file data/page_access_sequence.csv \
    --log-file data/logs/run1.log \
    --log-level INFO
```