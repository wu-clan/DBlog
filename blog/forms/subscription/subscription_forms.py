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


class UnSubscriptionForm(forms.Form):
    """
    取消邮件订阅
    """
    email = forms.CharField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}))
