# Workflow Test Task

## Requirements

1. python 3.11
2. Docker
3. Docker-compose

## Environmental variable

| Title                       | Default    | Description       | necessary |
|-----------------------------|------------|-------------------|----------|
| DB_HOST                     | localhost  | Database host     | yes      |
| DB_PORT                     | 5432       | Database port     | yes      |
| DB_DB                       | wd_wd      | Database name     | yes      |
| DB_USER                     | wd_user    | Database user     | yes      |
| DB_PASSWORD                 | wd_passord | Database password | yes      |


## Alembic

You can read information about migration and other in the [Alembic Readme.md](./alembic/README.md)

## Develop application

1. Install `docker` and `docker compose`
2. Run dev server `make up-build`
3. Run validation `make validation`

## How to use Pytest

1. Start dev server `make up-build`
2. Run pytest with command `make test`
