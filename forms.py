from django import forms #引入表单
from .models import ArticlePost #引入文章模型

class ArticlePostForm(forms.ModelForm):
	class Meta:
		model = ArticlePost
		fields = ('title','body')




