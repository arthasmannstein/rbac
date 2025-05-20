| Агрегированная роль | Атомарные роли |
|---------------------|----------------|
| ci-admin | gitlab-admin, nexus-admin |
| dev | gitlab-write, vault-read, nexus-write |
| infra-admin | ubuntu-admin, centos-admin |
| qa | gitlab-read, vault-read, nexus-read, grafana-read |
| readonly | gitlab-read, vault-read, grafana-read, zabbix-read, netdata-read, nexus-read |
| release-manager | gitlab-admin, vault-read, nexus-admin |
| support | zabbix-read, grafana-read, netdata-read |
| teamlead-dev | gitlab-write, gitlab-admin, vault-read, vault-write, nexus-write, grafana-read |
| vault-access | vault-read, vault-write |