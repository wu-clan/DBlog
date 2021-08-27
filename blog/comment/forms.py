# -*- coding: utf-8 -*-
from django import forms

from blog.models import Comment


class CommentForm(forms.ModelForm):
	"""
	评论扩展表单
	"""
	class Meta:
		model = Comment
		fields = (
			'user_name',
			'email',
			'url_input',
			'comment'
		)
