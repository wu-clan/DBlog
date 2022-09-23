# -*- coding: utf-8 -*-
"""
Django settings for djangoProject project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.contrib import admin

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v%!69-+jqak^*4b+y5uz_udp-l^#ii$6w)qrm&khj2anfc25z&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    # 第三方后台主题
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 消息
    'django.contrib.messages',
    # 静态文件
    'django.contrib.staticfiles',
    # 注册app
    'blog.apps.BlogConfig',
    # 后台快捷导入导出
    'import_export',
    # 第三方markdown
    'mdeditor',
    # 验证码
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 网站gzip压缩中间件
    'django.middleware.gzip.GZipMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']  # noqa
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 上下文处理器
                'blog.context_processors.sidebar',
                'blog.context_processors.website_conf',
                # templates中使用 {{ MEDIA_URL }}{{ 文件名 }} 拼接文件地址
                'django.template.context_processors.media',
            ],
            # 用于在模板中自动调用静态文件，不需要每个页面使用 {% load static %} 加载静态文件
            'builtins': [
                'django.templatetags.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}  # 字符集设置utf8mb4
    }
}

# redis 默认配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://""@127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
# 当你部署时，请使用 STATIC_ROOT
# 然后执行命令收集静态文件：python manage.py collectstatic --noinput
# STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

# Media path
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'static/media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# simpleui 排序后台app导航栏
SIMPLEUI_CONFIG = {
    'system_keep': True,
    'menu_display': ['文章配置', '网站配置信息', '文章订阅', '权限验证', ],
    'dynamic': True,
    'menus': [{
        'name': '文章配置',
        'models': [{
            'name': '文章大头图',
            'url': '/admin/blog/articleimg'
        }, {
            'name': '文章',
            'url': '/admin/blog/article'
        }, {
            'name': '文章类型',
            'icon': 'fa fa-list',
            'url': '/admin/blog/category'
        }, {
            'name': '标签',
            'icon': 'fa fa-tags',
            'url': '/admin/blog/tag'
        }, {
            'name': '评论',
            'icon': 'fa fa-comments',
            'url': '/admin/blog/comment'
        }]
    }, {
        'name': '网站配置信息',
        'models': [{
            'name': '网站基本配置',
            'url': '/admin/blog/conf'
        }, {
            'name': '首页轮播图配置',
            'url': '/admin/blog/carousel'
        }, {
            'name': '轮播公告',
            'icon': 'fas fa-bullhorn',
            'url': '/admin/blog/headannouncement'
        }, {
            'name': '主公告',
            'icon': 'fas fa-bullhorn',
            'url': '/admin/blog/mainannouncement'
        }, {
            'name': '友链',
            'icon': 'fa fa-link',
            'url': '/admin/blog/friend'
        }, {
            'name': '收款图',
            'icon': 'fa fa-coffee',
            'url': '/admin/blog/pay'
        }, {
            'name': "关于",
            'icon': 'fa fa-id-card',
            'url': '/admin/blog/about'
        }]
    }, {
        'name': '文章订阅',
        'models': [{
            'name': '订阅用户',
            'url': '/admin/blog/subscription'
        }]
    }, {
        'name': '权限验证',
        'icon': 'fas fa-user-shield',
        'models': [{
            'name': '用户',
            'icon': 'fa fa-user',
            'url': 'auth/user/'
        }, ]
    }]
}

# 网站默认配置
# 配置使用优先级：1.数据库(两分钟redis缓存), 2.本地
main_website = 'xwboy.top'
name = "CL' WU"
chinese_description = '永不放弃坚持就是这么酷！要相信光'
english_description = 'Never give up persistence is so cool！Believe in the light'
avatar_link = 'https://portrait.gitee.com/uploads/avatars/user/2194/6583646_wu_cl_1628047961.png!avatar200'
website_author = 'xiaowu'
website_author_link = 'https://www.xwboy.top'
email = '2186656812@qq.com'
website_number = '豫ICP备 2021019092号-1'
git = 'https://gitee.com/wu_cl'
website_logo = 'logo/DBlog.png'

# simpleui本地配置
SIMPLEUI_LOGO = 'https://www.xwboy.top/static/images/logo/DBlog.png' or 'https://www.xwboy.top/media/logo/DBlog.png'
SIMPLEUI_HOME_TITLE = 'DBlog后台管理'
SIMPLEUI_ANALYSIS = False
SIMPLEUI_LOADING = False
SIMPLEUI_DEFAULT_ICON = True
SIMPLEUI_HOME_INFO = False

# 后台header, title
admin.AdminSite.site_header = SIMPLEUI_HOME_TITLE
admin.AdminSite.site_title = SIMPLEUI_HOME_TITLE

# 登录后重定向到主页面
LOGIN_URL = '/blog/login'

# session设置
SESSION_COOKIE_AGE = 86400  # Session的cookie失效日期（秒）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期
SESSION_SAVE_EVERY_REQUEST = False  # 是否每次请求都保存Session，默认修改之后才保存

# 字母验证码
CAPTCHA_IMAGE_SIZE = (100, 36)  # 设置 captcha 图片大小
CAPTCHA_LENGTH = 4  # 字符个数
CAPTCHA_TIMEOUT = 3  # 超时(minutes)

# SMTP服务器
# 请更改为自己的邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_HOST_USER = 'xxx-nav@qq.com'
# 密码(请替换为你自己的哟) qq为设置=>账户=>POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务=> 开启服务POP3/SMTP服务=> 生成授权码
EMAIL_HOST_PASSWORD = 'xxxvszjyenrlvfkeaef'
# 发送邮件端口和加密
EMAIL_PORT = 465
EMAIL_USE_SSL = True
# 默认的发件人
DEFAULT_FROM_EMAIL = 'xiaowu的个人博客'
