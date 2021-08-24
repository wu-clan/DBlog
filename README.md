# Django博客系统

###### ps：项目处于试运行阶段，如果你想查看一版稳定的代码，请在标签中选择版本下载，如果你想查看实时状态的代码，请直接下载当前分支

[![python3](https://img.shields.io/badge/Python-3.8-red.svg)](https://www.python.org/downloads)
[![Django3.2](https://img.shields.io/badge/Django-3.2.4-green.svg)](https://docs.djangoproject.com/zh-hans/3.2)
[![simpleui](https://img.shields.io/badge/developing%20with-Simpleui-2077ff.svg)](https://github.com/newpanjing/simpleui)

🙈🙈🙈 使用Django快速搭建博客系统，采用Django框架最基础结构（仅一个app）

优点：减少逻辑性，便于入门学习...

缺点：内容沉余，不够灵活...

### 基本要求
* Python: 3.8
* Django: 3.2.4
* Mysql: 8
* Redis

### 示例博客：http://www.xwboy.top/ 

### 功能点
* markdown文章渲染，代码高亮，后台markdown编辑文章，个人信息等
* 文章分类，归档，快捷搜索，标签集
* 4 种皮肤（清新，清爽，简约，暗黑）自由切换
* 最新评论 / 阅读排行榜
* 多目标源博文分享（支持https）
* echarts 博文统计图（文章发布，分类，标签），雷达统计图（分类）
* 第三方社会化评论系统(畅言)
* 冷数据 redis 缓存
* windows: django-gzip压缩主站，linux: nginx-gzip压缩全站
* Rss / Atom 订阅
* 支持图床，后台上传图片可直链访问及调用  
* simpleui后台管理  +   后台自定义全站配置信息
* 用户注册，登录，注销，密码邮箱验证修改（非 django-auth 验证方式）

 _（持续更新ing...）_ 

###### ps: 如果访问网站期间，你使用了某些墙代理网络，会失去一些网页功能 ！！！

## ⬇ 源码下载
```
wget https://gitee.com/wu_cl/DBlog.git/master.zip
or
git clone https://gitee.com/wu_cl/DBlog.git
```

### 安装
```
1：pip install -r requirements.txt  # 安装所有依赖

2：创建数据库，修改setting.py mysql数据库配置 (创建数据库时记得选择 utf8mb4 编码)

2.5: 配置畅言：到 http://changyan.kuaizhan.com/ 注册站点,
将templates/blog/component/changyan.html中js部分换成你在畅言js。
畅言js位置: 畅言进入工作台->安装畅言->通用代码安装->自适应安装代码

3：python manage.py makemigrations
4：python manage.py migrate
5：python manage.py runserver
```

### 使用
```python
# 初始化用户名密码，按照提示输入用户名、邮箱、密码即可
python manage.py createsuperuser

# 登录后台 编辑类型、标签、发布文章等
http://127.0.0.1:8000/admin

# 常见报错：
django.db.utils.IntegrityError: (1048, "Column 'last_login' cannot be null")
执行 python manage.py migrate auth 后, 再创建用户即可
```
### END:
浏览器中打开 <http://127.0.0.1:8000/> 即可访问

## 🙏 搭建Linux服务端
```python
# 前提条件
你已经成功在windows部署并运行过DBlog项目

# 示例环境（全过程已示例环境为基础）
Ubuntu-20.04, nginx-1.18.0, uwsgi, mysql-8, python-3.8, redis-server

# linux文件夹中提供了配置的参考文件
nginx_conf: nginx 配置文件(https)
uwsgi.py: 开机自启动服务脚本
uwsgi.sh: 用于调用自启动服务脚本的shell脚本
```

### 环境准备
```python
已安装Ubuntu-20.04,进入linux系统,打开命令行窗口

1, cd /home, 将 windows 项目拷贝至 /home 目录下
   # 不建议直接将项目下载到linux，对于初学者，这是不友好的，
   # 可以下载和使用‘winscp’进行windows与linux之间的拖拽操作  

2, pip3 install uwsgi

3, 安装 mysql8 和 redis
   百度: Ubuntu-20.04 安装 mysql8 并创建数据库
   百度: Ubuntu-20.04 安装 redis

4, 将参考文件 nginx_conf 文件中的内容替换到 /etc/nginx/sites-enabled/default 文件中, 注意是替换内容,不是直接替换文件,如果网站未使用https,请百度django nginx配置,再修改文件内容

5, 将参考文件 uwsgi.sh 拷贝到 /etc/init.d/ 目录下, 并进入 /etc/init.d/ 目录执行 chmod 755 uwsgi.sh 赋予该脚本权限

ps: 之所以让百度,是因为细节太多了...
```

### 安装
```
1: cd /home/DBlog, 执行 pip install -r requirements.txt  # 安装所有依赖

2: 修改setting.py mysql数据库配置

3: python manage.py makemigrations
4: python manage.py migrate
5: python manage.py runserver
```

### 使用
```python
# 初始化用户名密码,按照提示输入用户名、邮箱、密码即可
python manage.py createsuperuser

# 登录后台 编辑类型、标签、发布文章等
http://服务器ip:8000/admin
```

### END:
浏览器中打开 <http://服务器ip:8000/> 即可访问

## ❓ 问题相关
欢迎提交问题到 [Issues](https://gitee.com/wu_cl/DBlog/issues) 
或我的QQ邮箱 `2186656812@qq.com`, 我将在看到问题后第一时间回复

### 学习交流群
应热爱学习的小伙伴, 我们也建群了, 这是一个New Group，期待并欢迎您的加入

有任何部署问题, 也可进群向我提问

![](readme/django_study.jpg)

[comment]: <> (## 🙇‍ 感谢)

[comment]: <> (☞ [jhao104]&#40;https://github.com/jhao104/django-blog&#41;)