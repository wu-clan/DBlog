from django.contrib import admin

# Register your models here.

from .models import Question

# 注册，使模型加入站点，可接受管理
admin.site.register(Question)