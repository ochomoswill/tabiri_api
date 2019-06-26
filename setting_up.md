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

### or

Create database

```sql
create database dbname;
```

Then grant superuser privileges to user

```sql
GRANT all privileges ON DATABASE dbname TO user;
```


Import database from sql file
`
psql -h hostname -d databasename -U username -f file.sql
`

Enable the postgis extension. Connect to psql then execute the below script

```shell
dbname=# CREATE EXTENSION postgis;
```


## API

Install virtualenvwrapper

```shell
sudo pip3 install virtualenvwrapper
```

Add config to .bashrc

```shell
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh
```

Create virtual env

```shell
mkvirtualenv tabiri_venv
```

To work on the tabiri_venv

```shell
workon tabiri_venv
```

Clone the api from the repo

```shell
git clone https://github.com/ochomoswill/tabiri_api.git
```

Move into the root directory of the project. Run the below command to install the required packages

```shell
pip3 install -r requirements.txt
```

Also install the below

```shell
pip install gunicorn psycopg2
```


Add the allowed hosts

```python
ALLOWED_HOSTS = ['your_server_domain_or_IP', 'second_domain_or_IP', . . .,'127.0.0.1',  'localhost']
```


Fake migrate
```shell
python manage.py migrate --fake
```

Testing Gunicorn's Ability to Serve the Project

go to the root directory of the project

```shell
gunicorn --bind 0.0.0.0:8000 tabiri_api.wsgi
```


### FAQ

After installing PostgreSQL I did the below steps. 


open the file pg_hba.conf for Ubuntu it will be in /etc/postgresql/9.x/main and change this line:
```text
local   all             postgres                                peer
```

to

```text
local   all             postgres                                trust
```


Restart the server

```bash
sudo service postgresql restart
```

Login into psql and set your password

```bash
psql -U postgres
```

```shell
dbname=# ALTER USER postgres with password 'your-pass';
```

Finally change the pg_hba.conf from

```text
local   all             postgres                                trust
```

to

```text
local   all             postgres                                md5
```

After restarting the postgresql server, you can access it with your own password

Authentication methods details:

*  trust - anyone who can connect to the server is authorized to access the database
*  peer - use client's operating system user name as database user name to access it.
*  md5 - password-base authentication




