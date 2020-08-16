## PostgreSQL Installation From Source Code on Remote Ubuntu 18.04 host
* [Requirements](https://www.postgresql.org/docs/current/install-requirements.html)
    + `sudo apt-get update`
    + `sudo apt install make`
    + `sudo apt install gcc`
    + `sudo apt install libreadline-dev libreadline7`
    + `sudo apt install zlib1g-dev`
* [Getting the Source](https://www.postgresql.org/docs/current/install-getsource.html)
    + `sudo wget  https://ftp.postgresql.org/pub/source/v12.3/postgresql-12.3.tar.gz`
    + `tar -xvzf postgresql-12.3.tar.gz`
* Make required sourcecode changes to collect the traces now
* [Installation Procedure](https://www.postgresql.org/docs/current/install-procedure.html)
    + './configure --enable-debug'
    + `make`
    + `sudo make install`

## Starting the PostgreSQL Server
* [PostgreSQL User Account](https://www.postgresql.org/docs/current/postgres-user.html)
    + `sudo adduser postgres`
* [Creating the Database Cluster](https://www.postgresql.org/docs/current/creating-cluster.html)
    + `./initdb -D /mydata/cpbptunexp/bench_clust_data`
* After configuring to accept remote connections - [Staring the Database Server](https://www.postgresql.org/docs/current/server-start.html)
    + `./pg_ctl -D /mydata/cpbptunexp/bench_clust_data start`
    + To restart the server use 'restart' in pg_ctl command

## Remote PostgreSQL Connection
* [Configure PostgreSQL to Accept Remote Connections](https://blog.bigbinary.com/2016/01/23/configure-postgresql-to-allow-remote-connection.html)
    + Copy over [pg_hba.conf](pg_hba.conf) and [postgresql.conf](postgresql.conf) into `/mydata/cpbptunexp/bench_clust_data`
* [Setting Admin User Password](https://stackoverflow.com/questions/7695962/postgresql-password-authentication-failed-for-user-postgres)
    + `./psql`
    + `ALTER USER postgres PASSWORD 'postgres_password';`
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
* To setup and populate tenant benchmark database (32 tenants)
    + `cp -R cpbpsim/utils/oltp_tenant_configs/ oltpbench/cpbptun_experiments`
    + `cp cpbpsim/utils/oltpbench_loader_32t.py oltpbench/`
    + `cd oltpbench`
    + `python3 oltpbench_loader_32t.py </dev/null &>loader.log &`
    + `disown`
* [Dump All Databases Before Running the Benchmarks](https://www.postgresql.org/docs/12/backup-dump.html)
    + `./pg_dumpall > /mydata/cpbptunexp/bench_clust_data/pg_dumpall_tpcc_32t.sql`
    + To download the dump, archive it first: `gzip pg_dumpall_tpcc_32t.sql`
* To run the benchmarks (16 tenants, for 3 hours)
    + Stop the database, clean the logs and restart the database
    + `cp cpbpsim/utils/oltpbench_launcher_16t_12s.py oltpbench/`
    + `cd oltpbench`
    + `python3 oltpbench_launcher_16t_12s.py </dev/null &>launcher.log &`
    + `disown`
    
## PostgreSQL Logs Processing
* Modify this [tool](../utils/pg_logs_to_pas_conv.py) to convert PostgreSQL logs into PAS file.

## Some Remote Host Management Stuff
* Cheking disks, their mountpoints and free space
    + `df -h` or `lsblk`
* [Mounting Disks](https://unix.stackexchange.com/questions/315063/mount-wrong-fs-type-bad-option-bad-superblock#315070)
* System Load Monitoring
    + `sudo apt install glances`
    + `glances`
* Granting access to folders
    + `sudo chmod -R a+rwx /path/to/folder/`
* Searching for suitable apt packages
    + `apt-cache search keyword`
* Manupilating many files at once
    + Renaming example: `for file in *100.xml; do mv "$file" "${file/100/40}"; done`
