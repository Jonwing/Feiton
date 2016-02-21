from django.contrib import admin
from pagedown.widgets import AdminPagedownWidget
from django import forms
from models import (
    Article,
    Author,
    Tag,
    Category,
    Statistic,
    Topset)
# Register your models here.


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

admin.site.register([
    Author,
    Tag,
    Category,
    Statistic,
    Topset
    ])
admin.site.register(Article, ArticleAdmin)
