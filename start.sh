#!/bin/bash

# 1. 登录相关配置
### 登录使用组件名称[bk_ticket]
export LOGIN_ACCOUNT_COMPONENT_NAME=""
### 登录PaaS平台鉴权URL
export LOGIN_AUTH_URL=""

# 2. 跨域相关配置
### 允许跨域的域名host,多个,分隔
export CORS_ALLOWED_HOSTS=""
### csrf_token的cookie的写入域名
export CSRF_COOKIE_DOMAIN=""

# 3. 系统初始化配置
### 系统运行环境
export RUNTIME_ENVIRONMENT="dev"
### 系统管理员,多个,分隔
export SUPERUSERS="xxx"
### 加密密钥
export SECRET_KEY="secret_key"
### 前端的登录路由
export FRONTEND_LOGIN_URL="xxx"

# 4. 环境配置启动
### mysql启动初始化
service mysql start
export MYSQL_DATABASE_NAME="dbs_mongo"
export MYSQL_ROOT_PASSWORD="root_test"
export MYSQL_USER="mongo"
export MYSQL_PASSWORD="mongo"
export MYSQL_HOST="localhost"
export MYSQL_PORT="3306"
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$MYSQL_ROOT_PASSWORD'"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE USER '$MYSQL_USER'@'localhost' IDENTIFIED WITH mysql_native_password BY '$MYSQL_PASSWORD'"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE_NAME DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE_NAME.* TO '$MYSQL_USER'@'localhost' WITH GRANT OPTION;"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "FLUSH PRIVILEGES;"
### 启动nginx
nginx
# 5. 服务进程初始化&启动
python manage.py migrate --no-input

python manage.py collectstatic --noinput
gunicorn wsgi -w 4 -b :5005
