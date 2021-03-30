from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    # this is a test
    path('', views.index, name='index'),
    # 详细文本内容
    path('<int:question_id>/', views.detail, name="detail"),
    # 问卷投票或调查结果
    path('<int:question_id>/results/', views.results, name='results'),
    # 投票动作
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

