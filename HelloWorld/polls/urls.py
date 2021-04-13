from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # this is a test
    path('', views.IndexView.as_view(), name='index'),
    # 详细文本内容
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    # 问卷投票或调查结果
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # 投票动作
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

