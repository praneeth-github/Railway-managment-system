# Railway Management System 

### Setting up MySQL 
```bash
create database railwaydb character set utf8;
create user stationuser@localhost identified by 'Password@0';
grant all privileges on railwaydb.* to stationuser@localhost;
flush privileges;
```

### Setting up Virtual Environment and Install Requirements
```bash
py -m venv new
new\Scripts\activate.ps1
```

### Running the project

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
