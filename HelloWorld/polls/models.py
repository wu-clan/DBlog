import datetime

from django.db import models
from django.utils import timezone
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('data published')

    # 打印出信息
    def __str__(self):
        return self.question_text

    # 判断是否当前时间段发布
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # 投票数
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

