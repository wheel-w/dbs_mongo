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
export RUNTIME_ENVIRONMENT="prod"
### 系统管理员,多个,分隔
export SUPERUSERS=""
### 加密密钥
export SECRET_KEY="this is a secret key"
### 前端的登录路由
export FRONTEND_LOGIN_URL="xxx"


# 4. 服务进程启动
python manage.py migrate --no-input

python manage.py collectstatic --noinput

gunicorn wsgi -w 4 -b :8000
