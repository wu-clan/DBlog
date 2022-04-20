from __future__ import unicode_literals

from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        """
        导入信号监听文件
        """
        import blog.signals