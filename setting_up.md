## Requirements

Requirements include:
* The Python programming language (Python > 3) 
* The Django web framework
* The PostgreSQL database for persisting data
* The PostGIS extension for supporting spatial features in the PostgreSQL database
* pip for installing dependencies
* The virtualenvwrapper module for managing a virtual environment

#### Install Python

First check if python is installed
`python3 --version`

If its not installed run
`sudo apt install python3`

#### Install dependencies of GeoDjango

```
sudo apt install gdal-bin libgdal-dev
sudo apt install python3-gdal
sudo apt install binutils libproj-dev
```

#### Install Postgres

```
sudo apt install python3-pip libpq-dev postgresql postgresql-contrib nginx curl
```

#### Install Postgis

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

#### Setting up the virtual environment

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

#### Setting up the project

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

#### Testing Gunicorn's Ability to Serve the Project

go to the root directory of the project

```shell
gunicorn --bind 0.0.0.0:8000 tabiri_api.wsgi
```


#### Creating systemd Socket and Service Files for Gunicorn

creating and opening a systemd socket file for Gunicorn

```shell
sudo nano /etc/systemd/system/gunicorn.socket
```

contents as below

```text
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

create and open a systemd service file for Gunicorn

```shell
sudo nano /etc/systemd/system/gunicorn.service
```

contents as below
```text
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=user_account_name
Group=www-data
WorkingDirectory=/home/user_account_name/myprojectdir
ExecStart=/home/user_account_name/.virtualenvs/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          djangoprojectname.wsgi:application

[Install]
WantedBy=multi-user.target
```

start and enable the Gunicorn socket
```shell
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

check the status of the Gunicorn service
```shell
sudo systemctl status gunicorn
```

you can test that the api is app by 
```shell
curl --unix-socket /run/gunicorn.sock 127.0.0.1:8000/api/gis/countries
```

If you make changes to the /etc/systemd/system/gunicorn.service file, reload the daemon to reread the service definition and restart the Gunicorn process by typing:
```shell
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```


#### Configure Nginx to Proxy Pass to Gunicorn

creating and opening a new server block in Nginx's sites-available directory:
```shell
sudo nano /etc/nginx/sites-available/myproject
```

content as below:

```text
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/user_account_name/myprojectdir;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```


enable the file by linking it to the sites-enabled directory

```shell
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

Test your Nginx configuration for syntax errors by typing:

```shell
sudo nginx -t
```

if no errors are reported, go ahead and restart Nginx by typing:

```shell
sudo systemctl restart nginx
```

Finally, we need to open up our firewall to normal traffic on port 80. Since we no longer need access to the development server, we can remove the rule to open port 8000 as well:

```shell
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```

### FYI

#### Database

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


#### API

If you update your Django application, you can restart the Gunicorn process to pick up the changes by typing:

```shell
sudo systemctl restart gunicorn
```

If you change Gunicorn socket or service files, reload the daemon and restart the process by typing:

```shell
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service
```


If you change the Nginx server block configuration, test the configuration and then Nginx by typing:

```shell
sudo nginx -t && sudo systemctl restart nginx
```




