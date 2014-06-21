#coding=utf8

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SignupForm(forms.Form):
    """用户注册"""
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("此用户名已存在,请使用其他名称")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("密码输入不一致，请重新输入")
        return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password1'])
        return new_user


class SigninForm(forms.Form):
    """用户登录"""
    username = forms.CharField(max_length=30)
    # email = forms.EmailField()
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def clean(self):
        clean = super(SigninForm, self).clean()
        username = clean.get('username')
        password = clean.get('password')
        if username and password:
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)
                if not (user and user.is_active):
                    raise forms.ValidationError("用户名或者密码错误！")
            else:
                raise forms.ValidationError("用户名不存在！")

        return clean


class PostNoteForm(forms.Form):
    title = forms.CharField(max_length=50, label='笔记标题')
    content = forms.CharField(widget=forms.Textarea, label='笔记内容')

    def clean(self):
        if not self.data.get('title'):
            raise forms.ValidationError("标题不能为空")
        if not self.data.get('content'):
            raise forms.ValidationError("笔记内容不能为空")

        return self.cleaned_data

