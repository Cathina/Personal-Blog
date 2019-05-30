# article/views.py

from django.shortcuts import render,redirect
from django.http import HttpResponse

from .models import ArticlePost,ArticleColumn
from .forms import ArticlePostForm
from django.contrib.auth.models import User

#引入markdown编辑器
import markdown

# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required

# 引入分页模块
from django.core.paginator import Paginator

from django.db.models import Q
# 引入 Q 对象

from comment.models import Comment

def article_list(request):
	search = request.GET.get('search')
	order = request.GET.get('order')
	column = request.GET.get('column')
	tag = request.GET.get('tag')

	article_list = ArticlePost.objects.all()

	if search and search != None and search != 'None':
		article_list = ArticlePost.objects.filter(
			Q(title__icontains=search) |
			Q(body__icontains=search)
			)
	else:
		search = '' #将search置空

	if column is not None and column.isdigit():
		article_list = article_list.filter(column=column)
	else:
		column = ''

	if tag and tag != 'None' and tag != None:
		article_list = article_list.filter(tags__name__in=[tag])
	else:
		tag = ''

	if order == 'total_views':
		article_list = article_list.order_by('-total_views')

	paginator = Paginator(article_list, 4)
	# 每页显示 4 篇文章
	page = request.GET.get('page')
	# 获取 url 中的页码
	articles = paginator.get_page(page)
	# 将导航对象相应的页码内容返回给 articles

	context = {'article_count':article_list,
				'articles':articles, 
				'order': order, 
				'search': search,
				'column':column,
				'tag':tag,}
	#需要传递给templates的对象
	return render(request,'article/list.html',context)
	#render函数：载入模版，返回context对象
	#render函数：request 固定对象， 定义模版文件位置、名称，context定义传入模版文件的上下文


def article_detail(request, id):
	article = ArticlePost.objects.get(id = id)
	#取出相应文章

	avatar = article.avatar

	comments = Comment.objects.filter(article=id)
	#取出文章评论

	tags = article.tags

	article.total_views += 1
	article.save(update_fields=['total_views'])
    # 浏览量 +1

	md = markdown.Markdown(
		extensions = [
		'markdown.extensions.extra',#包含 缩写、表格等常用扩展
		'markdown.extensions.codehilite',#语法高亮扩展
		'markdown.extensions.toc',# 目录扩展

		])
	#将markdown语法渲染成html样式

	article.body = md.convert(article.body)
	context = {'article':article, 
				'toc':md.toc, 
				'comments':comments,
				'avatar':avatar,
				}
	#取出context

	return render(request,'article/detail.html',context)
	#载入模版，返回context


def article_create(request):
	if request.method == "POST":
	#如果用户提交数据
		article_post_form = ArticlePostForm(request.POST, request.FILES)
		#将提交的数据赋值到表单实例中

		if article_post_form.is_valid():
		#如果提交的数据满足模型要求
			new_article = article_post_form.save(commit = False )
			#保存数据，但暂时不提交
			new_article.author = User.objects.get(id = request.user.id)

			if request.POST['column'] != 'none':
				new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
			new_article.save()
			#将新文章保存到数据库中

			article_post_form.save_m2m()
			# 保存tags 多对多关系
			return redirect("article:article_list")
			#返回到文章列表
		else:
		#数据不合法，返回错误信息
			return HttpResponse("表单内容有误，请重新填写！")


	else:
	#如果用户请求获取数据
		article_post_form = ArticlePostForm()
		#创建表单类实例
		columns = ArticleColumn.objects.all()
		context = {'article_post_form':article_post_form, 'columns':columns}
		#复制上下文
		return render(request,'article/create.html',context)
		#返回模版

@login_required(login_url='/userprofile/login/')	
def article_delete(request,id):
	#删除文章
	article = ArticlePost.objects.get(id=id)
	author = article.author

	if request.user == author:
		article.delete()
		return redirect("article:article_list")
	else:
		return HttpResponse("Sorry, permisson denied.")




@login_required(login_url='/userprofile/login/')
def article_update(request, id):
	"""
	更新文章的视图函数
	通过POST方法提交表单，更新titile、body字段
	GET方法进入初始表单页面
	id： 文章的 id
	"""
	# 获取需要修改的具体文章对象
	article = ArticlePost.objects.get(id=id)
	author = article.author

	if request.user == author:
		if request.method == "POST":# 判断用户是否为 POST 提交表单数据
			article_post_form = ArticlePostForm(data=request.POST)# 将提交的数据赋值到表单实例中

			if article_post_form.is_valid():# 判断提交的数据是否满足模型的要求
				article.title = request.POST['title']
				article.body = request.POST['body']

				if request.POST['column'] != 'none':
					article.column = ArticleColumn.objects.get(id=request.POST['column'])
				else:
					article.column = None

				article.save()

				return redirect("article:article_detail", id=id)
				# 完成后返回到修改后的文章中。需传入文章的 id 值
			
			else: # 如果数据不合法，返回错误信息
				return HttpResponse("表单内容有误，请重新填写。")

			# 如果用户 GET 请求获取数据
		else:
			article_post_form = ArticlePostForm()   
			columns = ArticleColumn.objects.all()    
			context = { 'article': article, 
						'article_post_form': article_post_form,
						'columns':columns, 
			}
			return render(request, 'article/update.html', context)

	else:
		#article_post_form = ArticlePostForm()       
		#context = { 'article': article, 'article_post_form': article_post_form }
		#return render(request, 'article/update.html', context)
		return HttpResponse("Sorry, permisson denied.")


