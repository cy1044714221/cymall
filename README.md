# cymall

 接口文档地址：https://docs.apipost.cn/preview/8db01ee5f6b4b970/cacf4cf6e235dd09

# 应用介绍

## users 用户目录

![UML 图 (1)](https://user-images.githubusercontent.com/33458444/152381810-f4f0f552-e7b0-435d-a181-cc8c1883f903.jpg)




# 错误代码
507  DatabaseError / RedisError
503 QQ 服务器异常


# QQ登陆

![UML 图 (2)](https://user-images.githubusercontent.com/33458444/152381721-e9da8707-fdb8-4fb2-97c8-a2b9e82e8240.jpg)

![流程图 (2)](https://user-images.githubusercontent.com/33458444/152381794-4c781fbd-fb45-49be-b7e6-db4725c821de.jpg)


# 部署

# python环境

**建立两个文件夹，用于存放virtualenv环境和项目**

\#放虚拟环境的

sudo mkdir -p /data/env

\#放项目的

sudo mkdir -p /data/wwwroot



**安装virtualenv**

sudo pip3 install virtualenv



cd /data/env

指定Python版本，创建名为cymall的虚拟环境，

sudo virtualenv -p /usr/bin/python3 cymall



**启动虚拟环境**

\#启动虚拟环境

source /data/env/cymall/bin/activate



**安装uwsgi**

sudo pip3 install uwsgi



# 安装Nginx

 sudo apt-get install nginx



# Django



直接运行测试 python manage.py rumserver 0:80



lsof -i :8000 查看端口占用

Kill -9 pid 

# 添加nginx 配置文件



```Groovy
cd /etc/nginx/sites-available

添加 cymall.conf 配置文件



添加软连接到 sites-enabled

(必须绿色 绝对位置)
ln -s /etc/ngix/sites-available/cymall.conf /etc/nginx/sites-enabled/cymall.conf
```

sudo vim /etc/nginx/sites-available/cymall.conf

```Nginx
server {
         listen  8000;
         charset   utf-8;
         server_name 124.223.90.3:8000;

         location / {
             include uwsgi_params;
             uwsgi_pass 124.223.90.3:8001;
         }
       
         location /static {
             alias /data/wwwroot/cymall/static; 
         }
    }



server {
  listen   80;
  server_name 124.223.90.3; 
  charset   utf-8;
  client_max_body_size 75M;  
  location /static {
     alias /data/wwwroot/cymall/static; 
  }

  
  error_page   500 502 503 504  /50x.html;
        location = /50x.html {
             root   html;
         }
}




```

# uwsgi

```
[uwsgi]
#使用nginx连接时使用，Django程序所在服务器地址
socket=:8001
#直接做web服务器使用，Django程序所在服务器地址
#http=10.211.55.2:8001
#项目目录
chdir= /data/wwwroot/cymall
#项目中wsgi.py文件的目录，相对于项目目录
wsgi-file=cymall/wsgi.py
# 进程数
processes=4
# 线程数
threads=2
# uwsgi服务器的角色
master=True
# 存放进程编号的文件
pidfile=uwsgi.pid
# 日志文件，因为uwsgi可以脱离终端在后台运行，日志看不见。我们以前的runserver是依赖终端的
daemonize=uwsgi.log
# 指定依赖的虚拟环境
virtualenv= /data/env/cymall
```



# 数据库

安装 mariadb 数据库 sudo apt-get install mariadb-server-10.3

查看运行状体啊。*service mariadb status*

查看版本 *mariadb -V*

启动 *service mariadb start*



## 配置数据库用户名 密码



CREATE USER 'cymall'@'%' IDENTIFIED BY 'password'; 

\#全部权限

grant all privileges on cymall.* to 'cymall'@'%';

grant all privileges on cymall.* to 'cymall'@'localhost';

\#指定权限

grant SELECT,UPDATE on 想授权的数据库.* to 'user1'@'%';





# 安装必要的包

```SQL
django~=3.2.5
djangorestframework~=3.13.1
django-ckeditor~=6.2.0
qqlogintool~=0.3.0
djangorestframework-jwt~=1.11.0
itsdangerous~=2.0.1
redis~=4.1.0
requests~=2.27.1
faker~=11.3.0

单独安装/ 没检测出来的依赖包
pip3 install celery
pip3 install django_redis
pip3 install Pillow
pip3 install drf-extensions
pip3 install python-alipay-sdk --upgrade
pip3 install django-simpleui
pip3 install django-cors-headers
pip3 install mysqlclient # 报错先：apt-get install libmysqlclient-dev



报错：
assert coreapi, '`coreapi` must be installed for schema support.'
AssertionError: `coreapi` must be installed for schema support.
pip install coreapi pyyaml





fastDFS 部署
pip3 install py3Fdfs
pip install mutagen
pip install requests
```



# Docker 部署fsatDFS

1、安装docker：sudo apt-get install -y docker.io

2、启动docker服务：systemctl start docker

3、设置开机启动：systemctl enable docker

拉取镜像sudo docker image pull delron/fastdfs

sudo docker run -dti --network=host --name tracker -v /var/fdfs/tracker:/var/fdfs delron/fastdfs tracker

sudo docker run -dti --network=host --name storage -e TRACKER_SERVER=124.223.90.3:22122 -v /var/fdfs/storage:/var/fdfs delron/fastdfs storage

# 安装redis

apt-get install redis

# 问题

部署 fastDFS 不能上传图片  开放23000端口

storage机器23000端口没有开启

https://blog.csdn.net/ever_siyan/article/details/88887450
