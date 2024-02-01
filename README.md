# Django博客系统

[![python3](https://img.shields.io/badge/Python-3.8-red.svg)](https://www.python.org/downloads)
[![Django3.2](https://img.shields.io/badge/Django-3.2-green.svg)](https://docs.djangoproject.com/zh-hans/3.2)
[![simpleui](https://img.shields.io/badge/developing%20with-Simpleui-2077ff.svg)](https://github.com/newpanjing/simpleui)

⚠️ 此项目已不再进行积极维护 ⚠️

🙈🙈🙈 使用Django快速搭建博客系统，采用Django框架基础结构（仅一个app）

优点：减少逻辑性，便于入门学习...

缺点：内容冗余，不够清晰...

### 技术栈

* Python: 3.8
* Django: 3.2
* Mysql: 8
* Redis
* Docker
* ......

### 示例博客：[点🤩我](http://www.xwboy.top/)

网站服务将于 2024-07-02 到期，届时网站将无法正常访问

<img src="static/images/show.png" alt="DBlog 首页">

### 功能点

* 用户注册，登录，登出，注销，密码邮箱验证重置
* markdown文章渲染，代码高亮，支持后台markdown编写文章等
* 文章分类，归档，快捷搜索，标签集
* 4 种皮肤（清新，清爽，简约，暗黑）切换
* 文章排行榜 / 最新评论 / 阅读量排行榜
* 博文评论系统
* 多目标源博文分享（支持https）
* echarts 统计图（雷达，折线，饼，梯形）
* windows: django-gzip压缩主站，linux: nginx-gzip压缩全站
* Rss / Atom 订阅
* Simpleui 后台管理

###### ps: 访问网站期间，使用墙代理网络或广告拦截插件，可能会丢失一些网站功能

## ⬇ 源码下载

```shell
wget https://gitee.com/wu_cl/DBlog.git/master.zip
# or
git clone https://gitee.com/wu_cl/DBlog.git
```

敏感词文件内容 static/sensitive_words/sensitive_words_lines.txt,
请前往 [sensitive_words](https://github.com/wjhgg/sensitive_words) 进行替换

## 使用

> [!WARNING]
> 此过程请格外注意端口占用情况, 特别是 8000, 3306, 6379...

### 1. 传统

1. 安装所有依赖
    ```shell
    pip install -r requirements.txt
    ```

2. 创建数据库 blog，选择 utf8mb4 编码
3. 检查并修改 djangoProject/settings.py mysql 数据库配置
4. 数据库迁移
   ```shell
   #  生成迁移文件
   python manage.py makemigrations
   
   # 执行迁移
   python manage.py migrate
   ```
5. 百度安装redis客户端, 安装完启动服务
6. 检查并修改 djangoProject/settings.py redis 数据库配置

### 2. docker

1. 在 docker-compose.yml 文件所在目录下执行一键启动命令

   ```shell
   docker-compose up -d --build
   ```

## 访问

创建管理员用户： `python manage.py createsuperuser`

后台：http://127.0.0.1:8000/admin

主页：http://127.0.0.1:8000

## 🙏 搭建Linux服务端

### 1. 传统

请移步 [wiki](https://gitee.com/wu_cl/DBlog/wikis/pages) 查看

### 2. docker

与 docker 使用方式相同

## 📨 互动

[WeChat / QQ](https://github.com/wu-clan)

## ❤️ 赞助

如果此项目能够帮助到你，你可以赞助作者一些咖啡豆表示鼓励：[:coffee: Sponsor :coffee:](https://wu-clan.github.io/sponsor/)
