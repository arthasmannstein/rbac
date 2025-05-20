# Access Model (RBAC)

Этот репозиторий содержит структуру ролевой модели доступа, построенной по принципу Role-Based Access Control (RBAC).  
Модель предназначена для машиночитаемого хранения, анализа, автоматизации и аудита прав доступа в инфраструктуре.

## Структура репозитория

```
access-model/
├── permissions/               # Атомарные разрешения (действие над сервисом)
│   ├── read-gitlab.md
│   ├── write-vault.md
│   └── ...
├── roles/
│   ├── atomic/                # Атомарные роли (1 разрешение = 1 роль)
│   │   ├── gitlab-read.md
│   │   ├── vault-write.md
│   ├── aggregated/            # Агрегированные роли (dev, qa и т.д.)
│   │   ├── dev.md
│   │   ├── teamlead-dev.md
│   ├── infrastructure/        # Инфраструктурные роли (ci-admin, vault-access)
│   │   └── [пока не реализовано]
│   ├── project/               # Проектные роли (scoped на конкретный проект)
│   │   └── [пока не реализовано]
├── matrix/                    # Excel-матрицы ролей и разрешений
│   ├── atomic_roles_matrix.xlsx
│   ├── aggregated_roles_matrix.xlsx
│   └── role_model_matrices_combined.xlsx
```

## Атомарные разрешения

Минимальная единица доступа: одно действие в одном сервисе.  
Например:

- read:gitlab — просмотр кода;
- write:vault — запись секретов;
- admin:ubuntu — root-доступ к ОС.

Они лежат в основе атомарных ролей.

## Атомарные роли (roles/atomic/)

Каждая атомарная роль — это обёртка над одним разрешением. Примеры:

- gitlab-read
- vault-write
- ubuntu-admin

Эти роли не назначаются напрямую конечным пользователям, а входят в агрегаты.

## Агрегированные роли (roles/aggregated/)

Роли, отражающие функции пользователей — разработчиков, тестировщиков, админов.  
Собираются из атомарных ролей.

Примеры:

- dev = gitlab-write, vault-read, nexus-write
- qa = gitlab-read, vault-read, grafana-read

Эти роли назначаются пользователям напрямую.

## Проектные и инфраструктурные роли

- roles/project/ — роли с ограниченным scope, например project-x-dev
- roles/infrastructure/ — роли для CI/CD, Vault, ОС и т.д.

Эти каталоги будут дополняться по мере развития модели.

## Матрицы

В matrix/ находятся Excel-файлы с матрицами:

- атомарная роль → разрешение;
- агрегированная роль → атомарные роли;
- комбинированная сводная таблица.

## Лицензия

MIT

## Вопросы или предложения?

Создайте issue или pull request.


<pre>
graph TD
  dev --> gitlab-write
  dev --> vault-read
  dev --> nexus-write
  qa --> gitlab-read
  qa --> vault-read
  qa --> nexus-read
  qa --> grafana-read
  ci-admin --> gitlab-admin
  ci-admin --> nexus-admin
  vault-access --> vault-read
  vault-access --> vault-write
  infra-admin --> ubuntu-admin
  infra-admin --> centos-admin
  support --> zabbix-read
  support --> grafana-read
  support --> netdata-read
  readonly --> gitlab-read
  readonly --> vault-read
  readonly --> grafana-read
  readonly --> zabbix-read
  readonly --> netdata-read
  readonly --> nexus-read
  teamlead-dev --> gitlab-write
  teamlead-dev --> gitlab-admin
  teamlead-dev --> vault-read
  teamlead-dev --> vault-write
  teamlead-dev --> nexus-write
  teamlead-dev --> grafana-read
  release-manager --> gitlab-admin
  release-manager --> vault-read
  release-manager --> nexus-admin
  </pre>