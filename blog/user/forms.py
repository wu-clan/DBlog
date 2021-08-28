# -*- coding: utf-8 -*-
from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms

from blog.models import UserInfo


class UserForm(forms.Form):
	"""
	用户表单
	"""
	username = forms.CharField(label="账号", max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label="密码", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	captcha = CaptchaField(label='验证码', widget=CaptchaTextInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
	"""
	注册表单
	"""
	username = forms.CharField(label="账号", max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password1 = forms.CharField(label="密码", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label="确认密码", max_length=16,
	                            widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
	captcha = CaptchaField(label='验证码', widget=CaptchaTextInput(attrs={'class': 'form-control'}))


class RestCodeForm(forms.Form):
	"""
	重置密码验证码表单
	"""
	username_email = forms.CharField(label='用户名或邮箱', max_length=16,
	                                 widget=forms.TextInput(attrs={'class': 'form-control'}))


class RestPwdForm(forms.Form):
	"""
	重置密码表单
	"""
	password1 = forms.CharField(label='新密码', max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label='确认新密码', max_length=16,
	                            widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	reset_code = forms.CharField(label='邮箱验证码', widget=forms.TextInput(attrs={'class': 'form-control'}))


class ProfileForm(forms.ModelForm):
	"""
	用户扩展信息表单
	"""

	class Meta:
		model = UserInfo
		fields = (
			'avatar',
			'mobile',
			'sex',
			'wechart',
			'qq',
			'blog_address',
			'introduction',
		)
