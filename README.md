# Railway Management System 

### Setting up MySQL 
```
create database railwaydb character set utf8;
create user stationuser1@localhost identified by 'Password@0';
grant all privileges on railwaydb.* to stationuser1@localhost;
flush privileges;
```

### Setting up Virtual Environment
```
py -m venv new
new\Scripts\activate.ps1
```

### Running the project
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
