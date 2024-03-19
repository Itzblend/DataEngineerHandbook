[Documentation](https://www.postgresql.org/docs/current/warm-standby.html#STANDBY-PLANNING)

Spin up your environment

```sh
docker-compose -f docker/docker-compose.yml up -d
```


Topics to understand:
- Master/Slave
- Write-Ahead Log (WAL)
- Synchronous & Asynchronous Replication
- Replication lag
- High Availability
- Point-in-time recovery


## Replication

### Primary server config

Create replica user
```sql
CREATE USER replicauser REPLICATION LOGIN ENCRYPTED PASSWORD 'replicapassword';
```

Edit the following parameters in your `postgresql.conf`
```sh
wal_level = logical replica?
wal_log_hints = on
max_wal_size = 1GB
hot_standby = on
```

Allow the replication connection to one or more servers in `pg_hba.conf`
```sh
host replication replicauser postgres-standby.docker_dbnet md5
host replication replicauser 172.25.0.1/32 md5
```

At this point restart the primary server or execute `SELECT pg_reload_conf();`

### Stand-by server config

Take the initial backup of the primary server
```sh
# https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-BASE-BACKUP
pg_basebackup -h localhost -p 5432 -U replicauser -X stream -C -S replica_1 -v -R -W -D ./docker/basebackup
```

Edit the host name of master to a hostname other containers can resolve
```sh
sed 's/localhost/primary-db/g' -i docker/basebackup/postgresql.auto.conf
```

Finally, launch a new postgres container with the base backup
```sh
docker run --rm --network docker_dbnet --name postgres-standby -e POSTGRES_PASSWORD=postgres -v ./docker/basebackup:/var/lib/postgresql/data  postgres:13
```

