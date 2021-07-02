## Django博客系统
![](https://img.shields.io/badge/Python-3.8-red.svg) 
![](https://img.shields.io/badge/Django-3.2.4-green.svg)
![](https://img.shields.io/badge/Powered%20by-2186656812@qq.com-blue.svg)

使用Django快速搭建博客

### 要求
* Python: 3.8
* Django: 3.2.4

### 示例博客：http://www.xwboy.top/

### 特点

* markdown 渲染，代码高亮
* 第三方社会化评论系统支持(畅言)
* 三种皮肤自由切换
* 阅读排行榜/最新评论
* 多目标源博文分享
* 博文归档
* 友情链接

### 下载
```
wget https://gitee.com/wu_cl/DBlog.git/master.zip
or
git clone https://gitee.com/wu_cl/DBlog.git
```

### 安装
```
pip install -r requirements.txt  # 安装所有依赖
修改setting.py配置数据库
配置畅言：到http://changyan.kuaizhan.com/注册站点,
将templates/blog/component/changyan.html中js部分换成你在畅言中生成的js。
畅言js位置: 畅言进入工作台-》安装畅言-》通用代码安装-》自适应安装代码

python manage.py makemigrations blog
python manage.py migrate
python manage.py runserver
```

### 使用

```python
# 初始化用户名密码
python manage.py createsuperuser
# 按照提示输入用户名、邮箱、密码即可
# 登录后台 编辑类型、标签、发布文章等
http://ip:port/admin

# 注：创建用户如果遇到以下报错：
# django.db.utils.IntegrityError: (1048, "Column 'last_login' cannot be null")
# 执行 python manage.py migrate auth 后，再新建用户即可
```

## 搭建Linux服务端
```python
示例环境: Ubuntu-20.04, nginx-1.18.0, uwsgi, mysql-8, python-3.8;
# 源码中给出了相关文件提供参考
# nginx_conf： nginx 配置文件
# uwsgi.ini： uwsgi.ini 配置文件
# uwsgi.py,uwsgi.sh  开机自启动服务脚本
环境准备:
1, 在目录 /home 下执行上文中的 下载 命令
2, apt-get 安装 uwsgi, nginx, mysql
3, 将 nginx_conf 中的内容替换到 /etc/nginx/sites-enabled/default
4, 将 uwsgi.sh 复制到 /etc/init.d/ 中, 执行 chmod 755 uwsgi.sh 赋予权限
5, 修改 default(nginx配置文件), 填写 server_name 为自己域名

# 环境准备过程中遇到的问题请自行百度！
```

### 安装，使用
```
同上，需要将 pip 改为 pip3，python 改为 python3 即可
```


浏览器中打开<http://127.0.0.1:8000/>即可访问