from django import forms

from .models import Article, BlogComment


# 用户意见
class ContactForm(forms.Form):

	user_name = forms.CharField(label='您的名字', max_length=50, initial='name', widget=forms.TextInput(attrs={"class": ""}))
	user_email = forms.EmailField(label='电子邮箱')
	user_number = forms.NumberInput()
	user_message = forms.CharField(label='内容', widget=forms.Textarea)


# 用户评论
class BlogCommentForm(forms.ModelForm):
	class Meta:
		model = BlogComment

		fields = ['user_name', 'user_email', 'body']

		widgets = {
			'user_name': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': "请输入昵称",
				'aria-describedby': "sizing-addon1",
			}),
			'user_email': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': "请输入邮箱",
				'aria-describedby': "sizing-addon1",
			}),
			'body': forms.Textarea(attrs={'placeholder': "我来评论两句~"})
		}
