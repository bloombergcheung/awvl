# awvl
Please open in google chrome
# Installing
## Clone the project
```
git clone https://github.com/bloombergcheung/awvl.git
cd awvl
```
## Install dependencies & activate virtualenv
```
conda create -n awvl python=3.11
conda activate awvl

pip install django
pip install PyMySQL
pip install django-redis
pip install pillow==9.5.0
```

## generate migration files & perform migration
```
python manage.py makemigrations
python manage.py migrate

```

## start redis
```
redis-server
redis-cli
```

## Running
```
python manage.py runserver
```

## 后台管理
```
localhost:8000/admin
创建超级管理员
python manage.py createsuperuser
```



