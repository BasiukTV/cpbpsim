## About
data_migration_policy.py contains classes used to determine the destination of page of data once said page is admitted or evicted from its current storage tier.
- Currently only contains ProbabilityBasedDataMigrationPolicy which determines the data page destination according to the preset probabilities and a uniform distribution of a random variable.

Also, when executed, will provide a data migration policy evaluation for a range of inputs.

## Code Usage Example
```
from data_migration_policy import ProbabilityBasedDataMigrationPolicy
dmp = ProbabilityBasedDataMigrationPolicy({
        "tiers" = ["SSD", "NVM", "RAM"],
        "data_admission_matrix" = [[0.0, 0.5, 0.5], [0.1, 0.0, 0.9], [0.0, 0.0, 1.0]],
        "data_eviction_matrix" = [[1.0, 0.0, 0.0], [0.9, 0.0, 0.1], [0.5, 0.5, 0.0]]})
print(dmp.destination_on_admission_from("SSD"))
print(dmp.destination_on_eviction_from("RAM"))
```

## Utility Usage Help
```
$ python3 data_migration_policy.py -h
```

## Utility Usage Examples
```
$ python3 data_migration_policy.py \
    --tiers SSD NVM RAM \
    --admission-matrix 0.0 0.5 0.5 0.1 0.0 0.9 0.0 0.0 1.0 \
    --eviction-matrix 1.0 0.0 0.0 0.9 0.0 0.1 0.5 0.5 0.0 \
    --admission-evaluations SSD 1000 NVM 1000 RAM 1000 \
    --eviction-evaluations SSD 1000 NVM 1000 RAM 1000 \
    > ../data_sets/new_data_migration_policy_evaluation_example.csv
```

## Generated File Example
[Example](../data_sets/data_migration_policy_evaluation_example.csv)
