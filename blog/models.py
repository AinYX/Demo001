from collections import defaultdict

from django.db import models
#
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
# Create your models here.


@python_2_unicode_compatible
class Article(models.Model):
	STATUS_CHOICES = (
		# 文章状态 草稿、发表
		('d', '草稿'),
		('p', '已发布'),
	)

	# 文章由标题（title）、正文（body）、创建时间（created_time）、修改时间（last_modified_time）、
	# 文章状态（status）、摘要（abstract）、浏览量（views)、点赞量（likes）、topped（置顶）
	# category  分类外键
	title = models.CharField('标题', max_length=70)
	body = models.TextField('内容')
	created_time = models.DateTimeField('创建时间', auto_now_add=True)      # 创建时自动加入时间
	last_modified_time = models.DateTimeField('修改时间', auto_now=True)    # 修改时自动修改时间
	status = models.CharField('文章状态', choices=STATUS_CHOICES, max_length=1)
	abstract = models.CharField('摘要', max_length=60, blank=True, null=True,
								help_text="")
	views = models.PositiveIntegerField('浏览量', default=0)
	likes = models.PositiveIntegerField('点赞数', default=0)
	topped = models.BooleanField('置顶', default=False)

	category = models.ForeignKey('Category', verbose_name='分类',null=True,
	                             on_delete=models.SET_NULL)
	# 文章的分类，ForeignKey即数据库中的外键。外键的定义是：如果数据库中某个表的列的值是另外一个表的主键。
	# 外键定义了一个一对多的关系，这里即一篇文章对应一个分类，而一个分类下可能有多篇
	# on_delete=models.SET_NULL表示删除某个分类（category）后该分类下所有的Article的外键设为null（空）

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('Blog:detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-last_modified_time']
		verbose_name = '博客数据'
		verbose_name_plural = verbose_name


class Category(models.Model):
	name = models.CharField('分类名字', max_length=20)
	created_time = models.DateTimeField('创建时间', auto_now_add=True)
	last_modified_time = models.DateTimeField('修改时间', auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('Blog:category', kwargs={'pk': self.pk})

	class Meta:
		verbose_name = '博客分类'
		verbose_name_plural = verbose_name

class About(models.Model):
	body = RichTextUploadingField()

	def __str__(self):
		return '关于我的内容'

	class Meta:
		verbose_name = '关于我'
		verbose_name_plural = verbose_name


class BlogComment(models.Model):
	user_name = models.CharField('评论者名字', max_length=100)
	user_email = models.EmailField('评论者邮箱', max_length=255)
	body = models.TextField('评论内容')
	created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
	article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

	def __str__(self):
		return self.body[:20]