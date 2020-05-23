## About
This tool generates the multi-tenant page access sequence to be used by a buffer pool simulator.

## Usage Help
```
python3 page_access_sequence_generator.py -h
```

## Usage Examples
```
$ python3 page_access_sequence_generator.py \
    --output ../../data/page_access_sequence.csv \
    --overwrite \
    --tenants 8 \
    --time 3600 \
    --time-offset 0 \
    --access-rate 1 1 2 2 4 4 8 8 \
    --access-distribution UNI PAR_1 UNI NOR_10 UNI PAR_2 UNI NOR_20 \
    --data-size 100 200 300 400 500 600 700 800 \
    --read-fraction 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8
```

## Console Output Example
```
For tenant #1, generating 3600 samples with uniform distribution for 100 pages and 0.1 fraction of reads.
For tenant #2, generating 3600 samples with Pareto (alpha=1) distribution for 200 pages and 0.2 fraction of reads.
For tenant #3, generating 7200 samples with uniform distribution for 300 pages and 0.3 fraction of reads.
For tenant #4, generating 7200 samples with normal (sigma=40) distribution for 400 pages and 0.4 fraction of reads.
For tenant #5, generating 14400 samples with uniform distribution for 500 pages and 0.5 fraction of reads.
For tenant #6, generating 14400 samples with Pareto (alpha=2) distribution for 600 pages and 0.6 fraction of reads.
For tenant #7, generating 28800 samples with uniform distribution for 700 pages and 0.7 fraction of reads.
For tenant #8, generating 28800 samples with normal (sigma=160) distribution for 800 pages and 0.8 fraction of reads.
Sorting samples according to their timestamps.
Writing out sorted samples to the file: ../data/new_page_access_sequence.dat
Done. Exiting!
```


## Generating Page Access Sequence with Time Offset
```
python3 page_access_sequence_generator.py \
    --output ../../data/time_offset_page_access_sequence_example.csv \
    --tenants 8 \
    --time 900 \
    --time-offset 0 \
    --access-rate 2 2 2 2 10 10 10 10 \
    --access-distribution NOR_10 NOR_10 NOR_10 NOR_10 PAR_2 PAR_2 PAR_2 PAR_2 \
    --data-size 200 200 200 200 1000 1000 1000 1000 \
    --read-fraction 0.2 0.2 0.2 0.2 0.1 0.1 0.1 0.1

python3 page_access_sequence_generator.py \
    --output ../../data/time_offset_page_access_sequence_example.csv \
    --tenants 8 \
    --time 900 \
    --time-offset 900 \
    --access-rate 2 2 2 4 10 10 10 20 \
    --access-distribution NOR_10 NOR_10 NOR_10 NOR_10 PAR_2 PAR_2 PAR_2 PAR_2 \
    --data-size 200 200 200 200 1000 1000 1000 1000 \
    --read-fraction 0.2 0.2 0.2 0.2 0.1 0.1 0.1 0.1

python3 page_access_sequence_generator.py \
    --output ../../data/time_offset_page_access_sequence_example.csv \
    --tenants 8 \
    --time 900 \
    --time-offset 1800 \
    --access-rate 2 2 4 2 10 10 20 10 \
    --access-distribution NOR_10 NOR_10 NOR_10 NOR_10 PAR_2 PAR_2 PAR_2 PAR_2 \
    --data-size 200 200 200 200 1000 1000 1000 1000 \
    --read-fraction 0.2 0.2 0.2 0.2 0.1 0.1 0.1 0.1

python3 page_access_sequence_generator.py \
    --output ../../data/time_offset_page_access_sequence_example.csv \
    --tenants 8 \
    --time 900 \
    --time-offset 2700 \
    --access-rate 1 1 2 2 5 5 10 10 \
    --access-distribution NOR_10 NOR_10 NOR_10 NOR_10 PAR_2 PAR_2 PAR_2 PAR_2 \
    --data-size 100 100 200 200 500 500 1000 1000 \
    --read-fraction 0.2 0.2 0.2 0.2 0.1 0.1 0.1 0.1

python3 page_access_sequence_generator.py \
    --output ../../data/time_offset_page_access_sequence_example.csv \
    --tenants 8 \
    --time 900 \
    --time-offset 3600 \
    --access-rate 2 2 2 2 10 10 10 10 \
    --access-distribution NOR_10 NOR_10 NOR_10 NOR_10 PAR_2 PAR_2 PAR_2 PAR_2 \
    --data-size 200 200 200 200 1000 1000 1000 1000 \
    --read-fraction 0.2 0.2 0.2 0.2 0.1 0.1 0.1 0.1
```

## Generated File Examples
[Simple Example](../../data/new_page_access_sequence.csv)
[Example with Time Offset](../../data/time_offset_page_access_sequence_example.csv)
