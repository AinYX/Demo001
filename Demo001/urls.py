"""Demo001 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^Blog/', include('Blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from login import views as login
from Blog import views as blog
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),

	# login
    url(r'^login/', login.login),
    url(r'^register/', login.register),
    url(r'^logout/', login.logout),
	url(r'^confirm/$', login.user_confirm),
	# 验证码
    url(r'^captcha', include('captcha.urls')),
	# 编辑器
	url(r'^ckeditor/', include('ckeditor_uploader.urls')),
	# Blog
	url(r'', include('Blog.urls', namespace='Blog', app_name='Blog')),

	url(r'', blog.index ),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
