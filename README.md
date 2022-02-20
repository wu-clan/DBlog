###### 📢❗❗❗ 2022.2.20 ❗❗❗ 
###### 今天做了一次小幅升级维护，如果你正在使用旧版本并且想更新到最新 master
```text
请提前备份你的迁移文件和已上传到media目录下的文件，为了避免不必要的问题，这是重要的
然后你需要执行如下: 
1: pip install -r requirements.txt
2: python manage.py makemigrations
3：python manage.py migrate
```
###### 你未在使用旧版本的话，直接按照安装使用说明部署即可

# Django博客系统

项目基本完成，处于试运行阶段，示例网站为当前分支最新代码，
如果您想查看旧版本，可以到标签中选择对应的版本进行下载

ps: 个人博客在一些逻辑和限制上面考虑还欠周全，存在bug，不影响正常使用，
后续开发已暂缓，欢迎 pull request，我将在审阅并测试后第一时间通知您

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
* 用户注册，登录，登出，注销，密码邮箱验证重置（非 django-auth 验证方式）
* markdown文章渲染，代码高亮，支持后台markdown编写文章等
* 文章分类，归档，快捷搜索，标签集
* 4 种皮肤（清新，清爽，简约，暗黑）切换
* 文章排行榜 / 最新评论 / 阅读量排行榜
* 博文评论系统（仅基本功能）
* 多目标源博文分享（支持https）
* echarts 博文发布，标签统计图（折线图，饼图，梯形图）
* 文章分类 雷达统计图（雷达图）
* 网站配置数据 redis 缓存
* windows: django-gzip压缩主站，linux: nginx-gzip压缩全站
* Rss / Atom 订阅
* 支持图床，后台上传图片可直链访问及调用
* simpleui后台管理


###### ps: 如果访问网站期间，你使用了某些墙代理网络，会失去一些网页功能 ！！！

## ⬇ 源码下载
```
wget https://gitee.com/wu_cl/DBlog.git/master.zip
or
git clone https://gitee.com/wu_cl/DBlog.git
```
敏感词文件内容 static/sensitive_words/sensitive_words_lines.txt,
请前往 [sensitive_words](https://github.com/wjhgg/sensitive_words) 进行替换

### 安装
```
1：pip install -r requirements.txt  # 安装所有依赖

2-1：创建数据库, 修改setting.py mysql数据库配置 (创建数据库时记得选择 utf8mb4 编码)
2-2: 百度安装redis客户端, 安装完启动服务即可

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

---
## 🙏 搭建Linux服务端
请移步 [wikis](https://gitee.com/wu_cl/DBlog/wikis/pages) 查看

## ❓ 问题相关
欢迎提交问题到 [Issues](https://gitee.com/wu_cl/DBlog/issues) 或我的QQ邮箱 `2186656812@qq.com`, 我将在看到问题后第一时间回复 