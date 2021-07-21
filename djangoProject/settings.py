"""
Django settings for djangoProject project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
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
	'simpleui',  # 第三方后台主题
	'import_export',  # 后台导入导出模块
	'mdeditor',  # 后台markdown编写文章模块
	# 'admin_reorder',  # 应用程序和模型的自定义排序组件...(更多:https://github.com/mishbahr/django-modeladmin-reorder)
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# 注册app
	'blog.apps.BlogConfig'
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	# 'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# 开启gzip压缩
	'django.middleware.gzip.GZipMiddleware',
	# 应用程序和模型的自定义排序组件...((更多:https://github.com/mishbahr/django-modeladmin-reorder))
	# 'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates']
		,
		'APP_DIRS': True,
		'OPTIONS': {
			# 用于模板自动调用到静态文件，而不需要再load
			'builtins': [
				'django.templatetags.static',
			],
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				# 上下文处理器
				'blog.context_processors.sidebar',
				'blog.context_processors.website_conf',
				# 用于在templates中直接调用{{ MEDIA_URL/文件名 }}拼接文件地址
				'django.template.context_processors.media',
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
		'HOST': 'localhost',
		'PORT': '3306'
	}
}

# redis配置
CACHES = {
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://""@127.0.0.1:6379/0",
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		}
	}
}
REDIS_TIMEOUT = 7 * 24 * 60 * 60
CUBES_REDIS_TIMEOUT = 60 * 60
NEVER_REDIS_TIMEOUT = 365 * 24 * 60 * 60

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

# 收集所有静态文件：python manage.py collectstatic
STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = (
	BASE_DIR / 'static',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'static/media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 网站默认配置
# 配置优先级：数据库(两分钟缓存), 本地
main_website = 'xwboy.top'
name = "CL' WU"
chinese_description = '永不放弃坚持就是这么酷！要相信光'
english_description = 'Never give up persistence is so cool！Believe in the light'
avatar_link = 'https://avatars.githubusercontent.com/u/52145145?v=4'
website_author = 'xiaowu'
website_author_link = 'http://www.xwboy.top'
email = '2186656812@qq.com'
website_number = '豫ICP备 2021019092号-1'
git = 'https://gitee.com/wu_cl'
website_logo = 'static/images/logo/DBlog.png'

"""
后台models自定义排序：(两个库都还有其他用法，请自行查看官方文档)
1，admin_reorder 第三方库
2，simpleui 第三方库集成

使用说明：
如果您使用 admin_reorder 排序，仅需注释掉 SIMPLEUI_CONFIG 字段即可
如果您使用 simpleui 排序，需要注释掉 [admin_reorder app + ModelAdminReorder 中间件]
"""
# admin_reorder 排序后台app导航栏
ADMIN_REORDER = (
	# Reorder app models
	{'app': 'blog', 'models': (
		'blog.Carousel',
		'blog.Announcement',
		'blog.Conf',
		'blog.Article',
		'blog.Category',
		'blog.Tag',
		'blog.Comment',
		'blog.Pay',
		'blog.Friend',
	)},
)

# simpleui 排序后台app导航栏
SIMPLEUI_CONFIG = {
	'system_keep': True,
	'menu_display': ['文章配置', '网站配置信息', '权限验证'],
	'dynamic': True,
	'menus': [{
		'name': '文章配置',
		'models': [{
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
			'url': '/admin/blog/carousel/'
		}, {
			'name': '公告',
			'icon': 'fas fa-bullhorn',
			'url': '/admin/blog/announcement/'
		}, {
			'name': '友链',
			'icon': 'fa fa-link',
			'url': '/admin/blog/friend'
		}, {
			'name': '收款图',
			'icon': 'fa fa-coffee',
			'url': '/admin/blog/pay'
		}]
	}, {
		'name': '权限验证',
		'icon': 'fas fa-user-shield',
		'models': [{
			'name': '用户',
			'icon': 'fa fa-user',
			'url': 'auth/user/'
		}, {
			'name': '用户组',
			'icon': 'fa fa-users',
			'url': 'auth/group/'
		}]
	}]
}

# simpleui本地配置
# SIMPLEUI_LOGO：对官方css进行了某些修改以适应后台尺寸，如果使用本源码，在 collectstatic 的时候请留意...
SIMPLEUI_LOGO = 'http://www.xwboy.top/static/images/logo/DBlog.png' or 'http://www.xwboy.top/media/logo/DBlog.png'
SIMPLEUI_HOME_TITLE = 'DBlog后台管理'
SIMPLEUI_ANALYSIS = False
SIMPLEUI_LOADING = False
SIMPLEUI_DEFAULT_ICON = True
SIMPLEUI_HOME_INFO = False

# 后台header, title
admin.AdminSite.site_header = SIMPLEUI_HOME_TITLE
admin.AdminSite.site_title = SIMPLEUI_HOME_TITLE