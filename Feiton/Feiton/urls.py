"""Feiton URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from Feiton.blog.views import ContactView

urlpatterns = [
    url(r"^$", 'Feiton.blog.views.index', name='home_page'),
    url(r"^about$", "Feiton.blog.views.about", name="about"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^post/', include('Feiton.blog.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r"^contact$", ContactView.as_view(), name="contact_me"),
]
