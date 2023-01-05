### 登录使用组件名称[bk_ticket]
export LOGIN_ACCOUNT_COMPONENT_NAME=""
### 登录PaaS平台鉴权URL
export LOGIN_AUTH_URL=""

### 系统的超级管理员,多个,分割
export SUPERUSERS=""

### 允许跨域的域名host,多个,分割
export CORS_ALLOWED_HOSTS=""

python manage.py migrate --no-input

python manage.py collectstatic --noinput

gunicorn wsgi -w 4 -b :8000
