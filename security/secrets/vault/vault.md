# Vault

Run up env
```sh
docker run --network docker_dbnet --cap-add=IPC_LOCK -e 'VAULT_LOCAL_CONFIG={"storage": {"file": {"path": "/vault/file"}}, "listener": [{"tcp": { "address": "0.0.0.0:8200", "tls_disable": true}}], "default_lease_ttl": "168h", "max_lease_ttl": "720h", "ui": true}' -p 8200:8200 vault server
```

```sh
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='<token>'
```

```sql
CREATE ROLE vaultuser WITH SUPERUSER CREATEROLE LOGIN PASSWORD 'vaultpass'
```

```sh
vault secrets enable database

vault write database/config/taxi \
    plugin_name="postgresql-database-plugin" \
    allowed_roles="taxi-reader" \
    connection_url="postgresql://{{username}}:{{password}}@primary-db:5432/taxi" \
    username="vaultuser" \
    password="vaultpass" \
    password_authentication="scram-sha-256"

vault write database/roles/taxi-reader \
    db_name="taxi" \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    revocation_statements="REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM \"{{name}}\"; DROP OWNED BY \"{{name}}\"; DROP ROLE \"{{name}}\";" \
    default_ttl="10m" \
    max_ttl="24h"

vault read database/creds/taxi-reader

```


## Disposable Database Credentials



## Policies
