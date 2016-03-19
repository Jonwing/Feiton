from django.contrib import admin
from models import (
    Article,
    Author,
    Tag,
    Category,
    Statistic,
    Topset)


admin.site.register([
    Article,
    Author,
    Tag,
    Category,
    Statistic,
    Topset
    ])
