from django.contrib import admin
from models import (
    Article,
    Author,
    Tag,
    Category,
    Statistic,
    Topset)
# Register your models here.

admin.site.register([
    Article,
    Author,
    Tag,
    Category,
    Statistic,
    Topset
    ])
