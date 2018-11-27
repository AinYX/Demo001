from django.conf.urls import url
from blog import views


urlpatterns = [
	url(r'^Blog/$', views.IndexView.as_view(), name='index'),
	# url(r'^Blog/test/(?P<article_id>\d+)$', views.Test.as_view(), name='detail'),
	url(r'^Blog/contact/$', views.def_contactview),
	url(r'^Blog/about/$', views.AboutView.as_view()),

	url(r'^Blog/detail/$', views.Detail.as_view(), name='detail_list'),
	url(r'^Blog/article/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name='detail'),
	url(r'^Blog/category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
]
