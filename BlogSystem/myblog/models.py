from django.db import models
from django.conf import settings

# Create your models here.

class TagName(models.Model):
    tag_name = models.CharField('标签名称', max_length=50)

    def __str__(self):
        return self.tag_name

class BlogSystem(models.Model):

    title = models.CharField(max_length=200)# 博客标题
    articletype = models.ForeignKey('Category', verbose_name='文章类型', on_delete=models.CASCADE)# 文章类型
    blog_time = models.DateField(auto_now_add=True)# 博客日期
    content_text = models.TextField()# 正文
    digest = models.TextField()# 文章摘要
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)# 作者
    readers = models.BigIntegerField(default=0)# 阅读数量
    comments = models.BigIntegerField(default=0)# 评论数量
    image_address = models.CharField(max_length=300)# 标题图片地址
    tag = models.ManyToManyField(TagName)# 标签
