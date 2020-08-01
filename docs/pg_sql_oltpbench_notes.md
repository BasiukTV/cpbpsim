## PostgreSQL Installation From Source Code
* [Requirements](https://www.postgresql.org/docs/current/install-requirements.html)
    + `sudo apt install make`
    + `sudo apt install gcc`
    + `sudo apt install libreadline-dev libreadline7`
    + `sudo apt-get install zlib1g-dev`
* [Getting the Source](https://www.postgresql.org/docs/current/install-getsource.html)
* [Installation Procedure](https://www.postgresql.org/docs/current/install-procedure.html)
    + To config use: './configure --with-blocksize=32 --with-wal-blocksize=64'

## Starting the PostgreSQL Server
* [PostgreSQL User Account](https://www.postgresql.org/docs/current/postgres-user.html)
    + `sudo adduser postgres`
* [Creating the Database Cluster](https://www.postgresql.org/docs/current/creating-cluster.html)
    + `./initdb -D /media/pg_data_ssd/bench_clust_data`
* [Staring the Database Server](https://www.postgresql.org/docs/current/server-start.html)
    + `./pg_ctl -D /media/pg_data_ssd/bench_clust_data/ start`
    + To restart the server use 'restart' in pg_ctl command

## Remote PostgreSQL Connection
* [Configure PostgreSQL to Accept Remote Connections](https://blog.bigbinary.com/2016/01/23/configure-postgresql-to-allow-remote-connection.html)
* [Setting Admin User Password](https://stackoverflow.com/questions/7695962/postgresql-password-authentication-failed-for-user-postgres)
    + `ALTER USER postgres PASSWORD 'Redsentrycrab14';`
* [PGAdmin Console](https://www.pgadmin.org/) used to connect to the database.

## Setting Up Tenant Databases
* Create a New DB User
    + `CREATE USER tpcc_user1 WITH PASSWORD 'tpcc_user1_password';`
* Create a New Database for the User
    + `CREATE DATABASE tpcc_db1;`
    + `GRANT ALL PRIVILEGES ON DATABASE tpcc_db1 to tpcc_user1;`

## Using OLTPBench to Run Benchmarks
* [OLTPBench wiki](https://github.com/oltpbenchmark/oltpbench/wiki)
    + `sudo apt install default-jre`
    + `sudo apt install ant`
    + `git clone https://github.com/oltpbenchmark/oltpbench.git`
    + `ant bootstrap`
    + `ant resolve`
    + `ant build`
* To setup and populate tenant benchmark database
    + `./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --create=true --load=true </dev/null &>/dev/null &`
    + `disown`
* To run the benchmark (for 300 seconds)
    + `./oltpbenchmark -b tpcc -c cpbptun_experiments/t1_flat.xml --execute=true -s 10 -o tpcc1_postgres_result </dev/null &>/dev/null &`
    + `disown`

## Some Azure Stuff
* [Mounting Disks](https://unix.stackexchange.com/questions/315063/mount-wrong-fs-type-bad-option-bad-superblock#315070)
* Granting access to folders
    + `sudo chmod -R a+rwx /path/to/folder/`

