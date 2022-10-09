"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),

    # 验证码
    path('captcha/', include('captcha.urls')),
    # markdown插件
    path('mdeditor/', include('mdeditor.urls')),
    # 处理静态文件
    path(r'static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}, ),
    # 处理图片文件
    path(r'media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}, ),
]

handler404 = views.page_not_found_error
