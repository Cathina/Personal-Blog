# article/admin.py

from django.contrib import admin

from .models import ArticlePost
from .models import ArticleColumn
#导入ArticlePost

admin.site.register(ArticlePost)
#注册ArticlePost到admin中

admin.site.register(ArticleColumn)
#注册ArticleColumn到admin中


# Register your models here.
