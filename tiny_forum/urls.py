"""tiny_forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from forum import views
from rest_framework import routers
import allauth

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'topics', views.TopicViewSet)
router.register(r'threads', views.ThreadViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'follows', views.FollowViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'', include(router.urls)),
    url(r'^api-auth/',
        include(
            'rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    # Example: summary/2016/08/28/
    url(r'^summary2/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.summary,
        name="analytics"),
]

# Required for gunicorn serving
urlpatterns += staticfiles_urlpatterns()
