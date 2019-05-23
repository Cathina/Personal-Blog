from django.shortcuts import render,redirect
from django.http import HttpResponse

from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.models import User
import markdown

# Create your views here.

def article_list(request):
	articles = ArticlePost.objects.all()
	#取出所有博客文章

	context = {'articles':articles }
	#需要传递给templates的对象

	return render(request,'article/list.html',context)
	#render函数：载入模版，返回context对象
	#render函数：request 固定对象， 定义模版文件位置、名称，context定义传入模版文件的上下文


def article_detail(request, id):
	article = ArticlePost.objects.get(id = id)
	#取出相应文章

	article.body = markdown.markdown(article.body,
		extensions = [
		'markdown.extensions.extra',#包含 缩写、表格等常用扩展
		'markdown.extensions.codehilite',#语法高亮扩展

		])
	#将markdown语法渲染成html样式

	context = {'article':article}
	#取出context

	return render(request,'article/detail.html',context)
	#载入模版，返回context


def article_create(request):
	if request.method == "POST":
	#如果用户提交数据
		article_post_form = ArticlePostForm(data = request.POST)
		#将提交的数据赋值到表单实例中

		if article_post_form.is_valid():
		#如果提交的数据满足模型要求
			new_article = article_post_form.save(commit = False )
			#保存数据，但暂时不提交
			new_article.author = User.objects.get(id = 1)
			#指定数据库中 id=1 的用户为作者
			#如果进行过删除数据表的操作，可能会找不到id为1的用户
			#此时重新创建用户，并传入此用户的id

			new_article.save()
			#将新文章保存到数据库中
			return redirect("article:article_list")
			#返回到文章列表
		else:
		#数据不合法，返回错误信息
			return HttpResponse("表单内容有误，请重新填写！")


	else:
	#如果用户请求获取数据
		article_post_form = ArticlePostForm()
		#创建表单类实例
		context = {'article_post_form':article_post_form}
		#复制上下文
		return render(request,'article/create.html',context)
		#返回模版

	
def article_delete(request,id):
	#删除文章
	article = ArticlePost.objects.get(id=id)
	#根据id获取待删除文章

	article.delete()

	return redirect("article:article_list")
	#返回文章列表

def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":

        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)

        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():

            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()

            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        article_post_form = ArticlePostForm()       
        context = { 'article': article, 'article_post_form': article_post_form }
        return render(request, 'article/update.html', context)

