from django.conf.urls import patterns, url, include
from django.contrib import admin

#from crawler import views

urlpatterns = patterns('',
    # home page
    url(r'^$', 'crawler.views.home', name="home"),
)

