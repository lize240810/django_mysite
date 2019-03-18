from django.urls import re_path, path
from . import views
'''
	投票应用的路由列表
'''

# 添加命名空间
app_name = 'polls'

# urlpatterns = [
#     re_path(r'^$', views.index, name="index"),
#     re_path(r'home', views.home, name="home"),
#     path(r'<int:question_id>/', views.datail, name='detail'),
#     path(r'<int:question_id>/results/', views.results, name="results"),
#     path(r'<int:question_id>/vote/', views.vote, name="vote"),
# ]
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
 	
#     # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]