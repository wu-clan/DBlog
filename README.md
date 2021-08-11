# Django博客系统 

（📢 _持续更新ing... 欢迎提交Issues..._ ）

[![python3](https://img.shields.io/badge/Python-3.8-red.svg)](https://www.python.org/downloads)
[![Django3.2](https://img.shields.io/badge/Django-3.2.4-green.svg)](https://docs.djangoproject.com/zh-hans/3.2)
[![simpleui](https://img.shields.io/badge/developing%20with-Simpleui-2077ff.svg)](https://github.com/newpanjing/simpleui)

🙈🙈🙈 使用Django快速搭建博客系统，采用Django框架最基础结构（仅一个app）

###### 优点：减少逻辑性，便于入门学习...

###### 缺点：内容沉余，不够灵活...

### 基本要求
* Python: 3.8
* Django: 3.2.4

### 示例博客：http://www.xwboy.top/ 

### 功能点

* markdown文章渲染，代码高亮，后台markdown编辑文章，个人信息等
* 文章分类，归档，快捷搜索，标签集
* 4 种皮肤（清新，清爽，简约，暗黑）自由切换
* 最新评论 / 阅读排行榜
* 多目标源博文分享（支持https）
* echarts 博文统计图（发布，分类，标签）
* 第三方社会化评论系统(畅言)
* 冷数据使用 redis 缓存
* windows:django-gzip压缩主站，linux:nginx-gzip压缩全站
* Rss / Atom 订阅
* 支持图床，后台上传图片可直链访问及调用  
* simpleui后台管理  +   后台自定义全站配置信息

 _（持续更新ing...）_ 

###### ps: 如果访问网站期间，你使用了某些墙代理网络，会失去一些网页功能 ！！！

## 源码下载
```
wget https://gitee.com/wu_cl/DBlog.git/master.zip
or
git clone https://gitee.com/wu_cl/DBlog.git
```

### 安装
```
1：pip install -r requirements.txt  # 安装所有依赖

2：修改setting.py mysql数据库配置

2.5:配置畅言：到http://changyan.kuaizhan.com/注册站点,
将templates/blog/component/changyan.html中js部分换成你在畅言中生成的js。
畅言js位置: 畅言进入工作台-》安装畅言-》通用代码安装-》自适应安装代码

3：python manage.py makemigrations blog (创建数据库时记得选择 utf8mb4 编码)
4：python manage.py migrate
5：python manage.py runserver
```

### 使用

```python
# 初始化用户名密码，按照提示输入用户名、邮箱、密码即可
python manage.py createsuperuser

# 登录后台 编辑类型、标签、发布文章等
http://ip:port/admin

# 注：创建用户如果遇到以下报错：
django.db.utils.IntegrityError: (1048, "Column 'last_login' cannot be null")
执行 python manage.py migrate auth 后，再新建用户即可
```
### END:
浏览器中打开 <http://127.0.0.1:8000/> 即可访问

## 🙏 搭建Linux服务端
```
示例环境 : （不同发行版本的linux之间命令方式可能存在细微差异,仅供参考）
Ubuntu-20.04, nginx-1.18.0, uwsgi, mysql-8, python-3.8, redis-server

# 在linux文件夹中给出了相关文件的提供参考
# nginx_conf： nginx 配置文件
# uwsgi.py： 开机自启动服务脚本
# uwsgi.sh:  用于调用自启动服务脚本的shell脚本

环境准备:
1, 进入目录 /home , 执行上文中的下载命令将项目下载到本地
2, pip3 install uwsgi
3, apt-get install mysql-server, redis-server
4, 将 nginx_conf 中的内容替换到 /etc/nginx/sites-enabled/default, 根据对网站的要求自行修改
5, 将 uwsgi.sh 复制到 /etc/init.d/ 中, 执行 chmod 755 uwsgi.sh 赋予权限

ps: 如果更改了 uwsgi 任一配置文件的位置，请记得修改配置文件里面的路径
```

### 安装，使用
```
步骤同上 ，注意需要将 pip 改为 pip3，python 改为 python3 ，再执行命令
```

## ❓问题相关

欢迎提交问题到 [Issus](https://gitee.com/wu_cl/DBlog/issues) 
或我的QQ邮箱 `2186656812@qq.com`, 我将在看到问题后第一时间回复

### 学习交流群
应热爱学习的小伙伴，我们也建群了，这是一个New Group，期待并欢迎您的加入

![](readme/django_study.jpg)

#### 🙇‍ 感谢
☞ [jhao104](https://github.com/jhao104/django-blog)