# article/models.py

from django.db import models

from django.contrib.auth.models import User
#导入内建User模型

from django.utils import timezone
#timezone 用于处理时间相关事务

from django.urls import reverse

from taggit.managers import TaggableManager

from PIL import Image

class ArticleColumn(models.Model):
    # 专栏 

    title = models.CharField(max_length=100,blank=True)
    # 栏目标题

    created = models.DateTimeField(default=timezone.now)
    # 创建时间

    def __str__(self):
        return self.title


# 博客文章数据模型
class ArticlePost(models.Model):

    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
        )
    # 文章栏目的一对多外键
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章作者。参数 on_delete 用于指定数据删除的方式

    title = models.CharField(max_length=100)
    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    
    body = models.TextField()
    # 文章正文。保存大量文本使用 TextField

    tags = TaggableManager(blank=True)
    # 文章标签。
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    # 文章标题图

    created = models.DateTimeField(default=timezone.now)
    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    
    updated = models.DateTimeField(auto_now=True)
    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间

    total_views = models.PositiveIntegerField(default=0)
    # 存储浏览量，PositiveIntegerField是用于存储正整数的字段，default=0设定初值为0

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
    #返回文章详情页面的url，实现路由重定向

    

    def save(self, *args, **kwargs):
    # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

    # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article








