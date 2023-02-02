FROM ubuntu:20.04

MAINTAINER wheel

RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tencent.com//#' /etc/apt/sources.list && sed -i 's#http://security.ubuntu.com/#http://mirrors.tencent.com//#' /etc/apt/sources.list

RUN apt-get update -y \
    && apt-get -y install iputils-ping \
    && apt-get -y install wget \
    && apt-get -y install net-tools \
    && apt-get -y install vim \
    && apt-get -y install openssh-server \
    && apt-get -y install python3.9 \
    && apt-get -y install python3-pip python3-dev \
    && apt-get -y install libpython3.9-dev \
    && apt-get -y install mysql-server \
    && apt-get -y install libmysqlclient-dev \
    && apt update \
    && apt -y install nginx \
    && cd /usr/local/bin \
    && rm -f python \
    && rm -f python3 \
    && rm -f pip \
    && rm -f pip3 \
    && ln -s /usr/bin/python3.9 python \
    && ln -s /usr/bin/python3.9 python3 \
    && ln -s /usr/bin/pip3 pip \
    && ln -s /usr/bin/pip3 pip3 \
    && python -m pip install --upgrade pip \
    && apt-get clean \
    && rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*

COPY docker_nginx.conf /etc/nginx/conf.d/static_service.conf

RUN mkdir -p /workspace/dbs-mongodb
COPY . /workspace/dbs-mongodb

RUN cd /workspace/dbs-mongodb && pip install -r requirements.txt -i https://mirrors.tencent.com/tencent_pypi/simple/

WORKDIR /workspace/dbs-mongodb
EXPOSE 5000
RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]