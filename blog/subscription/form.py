# -*- coding: utf-8 -*-
from django import forms

from blog.models import Subscription


class SubscriptionForm(forms.ModelForm):
	"""
	邮箱订阅表单
	"""
	class Meta:
		model = Subscription
		fields = (
			'email',
		)
