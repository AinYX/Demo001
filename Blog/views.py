from django.shortcuts import render, get_object_or_404, render_to_response
from django.shortcuts import redirect

from Blog.models import Article
from Blog.models import Category
from Blog.models import About
from .forms import BlogCommentForm

from django.views.generic import ListView, DetailView
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView

from django.views.decorators.csrf import csrf_exempt
import markdown2


# Create your views here.
class IndexView(ListView):
# 首页
	template_name = 'Blog/index.html'

	context_object_name = 'article_list'

	def get_queryset(self):

		article_list = Article.objects.filter(status='p', topped=True)

		for article in article_list:
			article.body = markdown2.markdown(article.body)

		return article_list

	def get_context_data(self, **kwargs):
		kwargs['category_list'] = Category.objects.all().order_by('name')

		return super(IndexView, self).get_context_data(**kwargs)


@csrf_exempt
def def_contactview(request):
# 联系我
	if request.method == 'POST':
		message = '感谢您的来信'
		user_name = request.POST['user_name']
		user_email = request.POST['user_email']
		user_number = request.POST['user_phone']
		user_message = request.POST['user_message']
		mail_body = u'''
	网友姓名：{}
	邮箱地址：{}
	电话号码：{}
	反映内容：
	{}
	'''.format(user_name, user_email, user_number, user_message)
		email = EmailMessage('来自【听风留博客】网站的网友意见', mail_body, user_email,
								['2579350980@qq.com'])
		email.send()
		return redirect('/Blog/')

	template = get_template('Blog/contact.html')
	request_context = RequestContext(request).push(locals())
	html = template.render(request_context)

	return HttpResponse(html)


class AboutView(ListView):
# 关于我
	template_name = 'Blog/about.html'

	context_object_name = 'about_list'

	def get_queryset(self):
		about_list = About.objects.all()

		return about_list


class ArticleDetailView(DetailView):
	# Django有基于类的视图DetailView,用于显示一个对象的详情页，我们继承它
	model = Article
	# 指定视图获取哪个model

	template_name = "Blog/article.html"
	# 指定要渲染的模板文件

	context_object_name = "article"
	# 在模板中需要使用的上下文名字

	pk_url_kwarg = 'pk'

	# 这里注意，pk_url_kwarg用于接收一个来自url中的主键，然后会根据这个主键进行查询
	# 我们之前在urlpatterns已经捕获article_id

	def get_object(self):
		obj = super(ArticleDetailView, self).get_object()
		obj.body = markdown2.markdown(obj.body)
		return obj

	def get_context_data(self, **kwargs):
		kwargs['category_list'] = Category.objects.all().order_by('name')
		article_list = Article.objects.filter(status='p')

		for article in article_list:
			article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)

		kwargs['article_list'] = article_list
		return super(ArticleDetailView, self).get_context_data(**kwargs)


class CategoryView(DetailView):
# 文章分类
	model = Category

	template_name = "Blog/category.html"
	# 指定需要渲染的模板

	context_object_name = "category"
	# 指定模板中需要使用的上下文对象的名字

	pk_url_kwarg = 'pk'

	def get_object(self):
		obj = super(CategoryView, self).get_object()
		obj.name = markdown2.markdown(obj.name)
		return obj

	# 给视图增加额外的数据
	def get_context_data(self, **kwargs):
		kwargs['category_list'] = Category.objects.all().order_by('name')
		kwargs['article_list'] = Article.objects.filter(category=self.kwargs['pk'],status='p')

		return super(CategoryView, self).get_context_data(**kwargs)



class Detail(ListView):
# 全部文章的显示
	template_name = "Blog/detail.html"

	context_object_name = "article_list"

	def get_queryset(self):
		article_list = Article.objects.filter(status='p')

		for article in article_list:
			article.body = markdown2.markdown(article.body)

		return article_list

	def get_context_data(self, **kwargs):
		kwargs['category_list'] = Category.objects.all().order_by('name')

		return super(Detail, self).get_context_data(**kwargs)

"""
def detail(request, pk):
	article = get_object_or_404(Article, pk=pk)
	return render(request, 'blog/detail.html', context={'post': article})
"""


class CommentPostView(FormView):
# 处理评论的数据
	form_class = BlogCommentForm    # 指定用哪一个Form(记得把form导入)

	template_name = 'Blog/article.html' # 指定评论提交成功后跳转渲染的网页

	def form_valid(self, form):
		"""提交的数据验证合法后要处理的事情"""
		# 根据url传过来的参数(判断self.kwargs['article_id']被评论的是哪一篇文章)
		target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])

		# 调用FormView的save方法实例化comment   设置(commit=False)就是先不保存到数据库
		comment = form.save(commit=False)

		# 把评论的所属文章关联起来  然后再保存到数据库
		comment.article = target_article
		comment.save()


		self.success_url = target_article.get_absolute_url()
		return HttpResponseRedirect(self.success_url)

	def form_invalid(self, form):
		target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])

		return render(self.request, 'Blog/article.html', {
			'form': form,
			'article': target_article,
			'comment_list': target_article.blogcomment_set.all(),
		})


def index(request):
# 主页跳转
	return redirect('/Blog/')
	return render_to_response()
