from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length = 50)  #博客题目
    category = models.CharField(max_length = 50, blank = True)  #博客标签
    author = models.CharField(max_length = 20)  #博客作者
    date_time = models.DateTimeField(auto_now_add = True)  #博客日期
    content = models.TextField(blank = True, null = True)  #博客文章正文

    def __unicode__(self) :  #函数article对象要怎么表示自己：用title字段表示
        return self.title

    class Meta:  #按时间下降降序
        ordering = ['-date_time']


#CharField 存储字符串
#TextField 存储大量文本
#DateTimeField 存储时间 auto_now_add = True自动设置对象增加时间
