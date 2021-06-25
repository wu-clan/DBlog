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
from django.urls import path, include
from django.contrib import admin
from django.views.static import serve

from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('', views.index, name='index'),

    # path(r'^static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}, name='online_static'),  # 处理静态文件(用于上线环境)
    path(r'^media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT},),  # 处理图片文件
]


handler404 = views.page_not_found_error
handler500 = views.page_error
