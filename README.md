# Railway Management System 


## Install components
```bash
sudo apt-get update
sudo apt-get install python-pip python-dev mysql-server libmysqlclient-dev

```

### Setting up MySQL 
```bash
sudo mysql_secure_installation
mysql -u root -p
create database railwaydb character set utf8;
create user stationuser@localhost identified by 'Password@0';
grant all privileges on railwaydb.* to stationuser@localhost;
flush privileges;
exit
```

### Setting up Virtual Environment and Install Requirements
```bash
sudo pip install virtualenv
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
```

### Running the project

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


