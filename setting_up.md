## Requirements

Requirements include:
* The Python programming language (Python > 3) 
* The Django web framework
* The PostgreSQL database for persisting data
* The PostGIS extension for supporting spatial features in the PostgreSQL database
* pip for installing dependencies
* The venv module for managing a virtual environment

1. Install Python

First check if python is installed
`python3 --version`

If its not installed run
`sudo apt install python3`

2. Install dependencies of GeoDjango

```
sudo apt install gdal-bin libgdal-dev
sudo apt install python3-gdal
sudo apt install binutils libproj-dev
```

3. Install Postgres

```
sudo apt install python3-pip libpq-dev postgresql postgresql-contrib nginx curl
```

4. Install Postgis

```shell
sudo apt-get install postgis
```



## Database

Export database

`pg_dump -U username -h localhost databasename >> sqlfile.sql
`

### Import database

Change user to postgres

`
su - postgres
`

Create user

`createuser --interactive --pwprompt`

Create database

`createdb -O user dbname`

Import database from sql file
`
psql databasename < path_to_sql_file
`

Enable the postgis extension. Connect to psql then execute the below script

```shell
dbname=# CREATE EXTENSION postgis;
```