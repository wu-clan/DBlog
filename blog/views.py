# -*- coding: utf-8 -*-
# Create your views here.
import os
import re

import markdown
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from fast_captcha import tCaptcha
from markdown.extensions.toc import TocExtension

from blog.forms.comment.comment_forms import CommentForm
from blog.forms.subscription.subscription_forms import SubscriptionForm, UnSubscriptionForm
from blog.forms.user.user_forms import EditUserInfo, ProfileForm, RegisterForm, RestCodeForm, RestPwdForm, UserForm
from blog.models import About, Subscription
from blog.models import Article, Category, Tag, UserInfo
from djangoProject import settings
from djangoProject.settings import SESSION_COOKIE_AGE
from djangoProject.utils.comments_check import DFAFilter
from djangoProject.utils.get_request_address import get_req_info
from djangoProject.utils.pagination import PageInfo


def index(request):
    """
    主页
    """
    _blog_list = Article.objects.all().order_by('-date_time')[0:5]
    _blog_hot = Article.objects.all().order_by('-view')[0:3]
    return render(request, 'blog/index.html', {"blog_list": _blog_list, "blog_hot": _blog_hot})


def get_page(request):
    """
    分页
    """
    page_number = request.GET.get("page")
    return 1 if not page_number or not page_number.isdigit() else int(page_number)


def user_login(request):
    """
    用户登录
    """
    # 登录请求
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            login_user = User.objects.filter(username=username)
            if not login_user.exists():
                messages.error(request, "用户不存在~")
                return redirect(reverse('blog:login'))
            if not login_user.first().is_active:
                messages.error(request, '用户已被锁定，请联系管理员')
                return redirect('blog:login')
            user = authenticate(username=username, password=password)
            if user:
                # 自动登录并存储session
                login(request, user)
                next_url = request.POST.get('next', reverse('index'))
                return redirect(next_url)
            else:
                messages.error(request, "密码输入有误。请重新输入~")
        else:
            messages.error(request, '验证码错误')
    else:
        login_form = UserForm()
    return render(request, 'blog/user/login.html', locals())


def user_register(request):
    """
    用户注册
    """
    # 注册请求
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            if data.get('password1') != data.get('password2'):
                messages.error(request, '密码输入不一致，请重新输入')
                return redirect(reverse('blog:register'))
            else:
                same_name = User.objects.filter(username=data.get('username'))
                if same_name:
                    messages.error(request, '用户名已存在，请重新输入')
                    return redirect(reverse('blog:register'))
                same_email = User.objects.filter(email=data.get('email'))
                if same_email:
                    messages.error(request, '邮箱已被注册，请重新输入')
                    return redirect(reverse('blog:register'))
                # 注意创建用户用法
                new_user = User.objects.create_user(username=data.get('username'), password=data.get('password2'),
                                                    email=data.get('email'))
                new_user.save()
                messages.success(request, '注册成功，现在可以登陆啦')
                return redirect(reverse('blog:login'))
    else:
        register_form = RegisterForm()
    return render(request, 'blog/user/register.html', locals())


def password_reset(request):
    """
    密码重置
    """
    return render(request, 'blog/password_reset/password_reset.html')


def password_reset_email(request):
    """
    密码重置验证码
    """
    if request.method == "POST":
        rest_pwd_form = RestCodeForm(request.POST)
        if rest_pwd_form.is_valid():
            username_email = rest_pwd_form.cleaned_data['username_email']
            # 调试的时候请将此 try 方法注释，改为只是用 if 判断
            try:
                user = User.objects.filter(Q(username=username_email) | Q(email=username_email))
                if user:
                    mail_receiver = user[0].email
                    email_title = "重置密码"
                    code = tCaptcha()  # 验证码
                    del request.session["tCaptcha"]
                    request.session["tCaptcha"] = code  # 将验证码保存到session
                    email_body = F"您的重置密码验证码为：{code}\n" \
                                 F"为了不影响您正常使用，请在{SESSION_COOKIE_AGE / 60}分钟之内完成密码重置"
                    send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, (mail_receiver,),
                                            auth_user=settings.EMAIL_HOST_USER,
                                            auth_password=settings.EMAIL_HOST_PASSWORD)
                    messages.success(request, "验证码已发送，请查收邮件")
                    return redirect(reverse('blog:password_reset_base'))
            except Exception:
                messages.error(request, '验证码发送失败，请联系网站管理员吧')
            else:
                messages.error(request, '用户名或邮箱不存在')
    else:
        rest_pwd_form = RestCodeForm()
    return render(request, 'blog/password_reset/password_reset_email.html', locals())


def password_reset_base(request):
    """
    密码重置主页
    """
    if request.method == 'POST':
        rest_pwd_form = RestPwdForm(request.POST)
        if rest_pwd_form.is_valid():
            password1 = rest_pwd_form.cleaned_data['password1']
            password2 = rest_pwd_form.cleaned_data['password2']
            code = rest_pwd_form.cleaned_data['reset_code']
            if password1 == password2:
                if code == request.session["tCaptcha"]:
                    new_user = User.objects.update(
                        password=make_password(password2)
                    )
                    del request.session["tCaptcha"]
                    return redirect(reverse('blog:password_reset_done'))
                else:
                    messages.error(request, '验证码错误')
            else:
                messages.error(request, '密码输入不一致，请重新输入')
    else:
        rest_pwd_form = RestPwdForm()
    return render(request, 'blog/password_reset/password_reset_base.html', locals())


def password_reset_done(request):
    """
    重置结束
    """
    return render(request, 'blog/password_reset/password_reset_done.html')


@login_required
def user_logout(request):
    """
    用户退出
    """
    logout(request)
    return redirect('/blog')


def user_delete(request, pk):
    """
    用户注销
    """
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        if request.user == user:
            # 注销用户，返回主页
            request.session.flush()
            user.delete()
            messages.success(request, '注销账户成功')
            return redirect('/blog')
        else:
            messages.error(request, '非注销账户登录，您没有权限执行注销操作')
            return redirect('/blog')
    else:
        return redirect('/blog')


# 编辑用户信息
@login_required
def profile_edit(request, pk):
    user = User.objects.get(id=pk)
    old_username = user.username
    old_email = user.email
    userinfo = UserInfo.objects.get(user_id=pk)
    if request.method == 'POST':
        if request.user != user:
            messages.error(request, '你没有权限修改此用户信息')
            return redirect('blog:edituser', pk=pk)
        # 更新邮箱
        user_form = EditUserInfo(request.POST)
        # 更新用户信息
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            if username != old_username:
                user_username = User.objects.filter(username=username)
                if user_username:
                    messages.error(request, f'用户名 {username} 已经被注册过了，请更换用户名后重新提交！')
                    return redirect('blog:edituser', pk=pk)
                user.username = username
                user.save()
            if email != old_email:
                user_email = User.objects.filter(email=email)
                if user_email:
                    messages.error(request, f'邮箱地址 {email} 已经被注册过了，请更换邮箱地址后重新提交！')
                    return redirect('blog:edituser', pk=pk)
                user.email = email
                user.save()
        if profile_form.is_valid():
            profile_form.save(commit=False)
            data = profile_form.cleaned_data
            if data.get('mobile') is not None:
                tel_re = re.compile(r"^1[3-9]\d{9}$")
                if not tel_re.findall(str(data.get('mobile'))):
                    messages.error(request, '手机号码格式错误')
                    return redirect('blog:edituser', pk=pk)
            if 'avatar' in request.FILES:
                try:
                    # 删除旧头像文件
                    os.remove(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, str(userinfo.avatar)))
                except OSError or FileNotFoundError:
                    pass
                userinfo.avatar = data['avatar']
                # 同步更新用户所有评论头像地址
                comment_avatar = user.comment_user.filter(user=user.id)
                cmt_ava = comment_avatar.exists()
                if cmt_ava:
                    comment_avatar.all().update(avatar_address=data['avatar'])
            userinfo.mobile = data['mobile']
            userinfo.wechat = data['wechat']
            userinfo.qq = data['qq']
            userinfo.blog_address = data['blog_address']
            userinfo.introduction = data['introduction']
            userinfo.save()
            messages.success(request, '更新个人信息成功')
            return redirect('blog:edituser', pk=pk)
        else:
            messages.error(request, '表单输入错误，更新用户信息失败')
            return redirect('blog:edituser', pk=pk)
    else:
        user_form = EditUserInfo()
        profile_form = ProfileForm()
    return render(request, 'blog/user/edituser.html', locals())


""""""""""""""""""""""""" 登录结束 """""""""""""""""""""""""


def detail(request, pk):
    """
    博文详情
    """
    blog = get_object_or_404(Article, pk=pk)
    blog.viewed()
    # Markdown渲染文章(含目录)，注意Markdown的 M 大小写
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            TocExtension(slugify=slugify),
        ]
    )
    # md文章内容
    blog.content = md.convert(blog.content)
    # 获取对应文章的全部评论，倒序显示
    comments = blog.post.all().order_by('-create_time')
    context = {
        "blog": blog,
        'toc': md.toc,
        'comments': comments
    }
    return render(request, 'blog/detail.html', context=context)


def blog_list(request):
    """
    文章列表
    """
    page_number = get_page(request)
    blog_count = Article.objects.count()
    page_info = PageInfo(page_number, blog_count)
    _blog_list = Article.objects.all()[page_info.index_start: page_info.index_end]
    return render(request, 'blog/list.html', {"blog_list": _blog_list, "page_info": page_info})


def category(request, name):
    """
    文章分类
    """
    categories = Category.fetch_all_category()
    page_number = get_page(request)
    blog_count = Article.objects.filter(category__name=name).count()
    page_info = PageInfo(page_number, blog_count)
    _blog_list = Article.objects.filter(category__name=name)[page_info.index_start: page_info.index_end]
    return render(request, 'blog/category.html', {
        "blog_list": _blog_list,
        "page_info": page_info,
        "category": name,
        'categories': categories
    })


def tag(request, name):
    """
    标签
    """
    page_number = get_page(request)
    blog_count = Article.objects.filter(tag__tag_name=name).count()
    page_info = PageInfo(page_number, blog_count)
    _blog_list = Article.objects.filter(tag__tag_name=name)[page_info.index_start: page_info.index_end]
    return render(request, 'blog/tag.html', {
        "blog_list": _blog_list,
        "tag": name,
        "page_info": page_info
    })


def archive(request):
    """
    文章归档
    """
    _blog_list = Article.objects.values("id", "title", "date_time").order_by('-date_time')
    archive_dict = {}
    for blog in _blog_list:
        pub_month = blog.get("date_time").strftime("%Y年%m月")
        if pub_month in archive_dict:
            archive_dict[pub_month].append(blog)
        else:
            archive_dict[pub_month] = [blog]
    data = sorted([{"date": _[0], "blogs": _[1]} for _ in archive_dict.items()], key=lambda item: item["date"],
                  reverse=True)
    return render(request, 'blog/archive.html', {"data": data})


def about(request):
    """
    关于（包含统计图）
    """
    # markdown渲染自我介绍
    about_text = About.objects.all().first()
    if about_text:
        about_text.contents = markdown.markdown(about_text.contents, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
        ])
    # 统计图准备
    articles = Article.objects.filter().all().order_by('-date_time')
    categories = Category.fetch_all_category()
    if not articles or not categories:
        # 没有文章或者分类的情况
        return render(request, 'blog/about.html', {'articles': None, 'categories': None})
    # 发布统计
    all_date = articles.values('date_time')
    # 计算最近一年的时间list作为坐标横轴 注意时间为 例如[2019-5] 里面不是2019-05
    latest_date = all_date[0]['date_time']
    end_year = latest_date.strftime("%Y")
    end_month = latest_date.strftime("%m")
    date_list = []
    for i in range(int(end_month), 13):
        date = str(int(end_year) - 1) + '-' + str(i)
        date_list.append(date)
    for j in range(1, int(end_month) + 1):
        date = end_year + '-' + str(j)
        date_list.append(date)
    value_list = []
    all_date_list = []
    for i in all_date:
        # 这里直接格式化 去掉月份前面的0, !! window使用%#m, mac和linux使用%-m !!
        try:
            all_date_list.append(i['date_time'].strftime('%Y-%-m'))
        except ValueError:
            all_date_list.append(i['date_time'].strftime('%Y-%#m'))
    for i in date_list:
        value_list.append(all_date_list.count(i))

    # 饼图统计
    temp_list = []  # 临时集合
    tags_list = []  # 存放每个标签对应的文章数
    tags = Tag.objects.all()
    for tag in tags:
        temp_list.append(tag.tag_name)
        temp_list.append(len(tag.article_set.all()))
        tags_list.append(temp_list)
        temp_list = []
    # 根据文章数排序
    tags_list.sort(key=lambda x: x[1], reverse=True)

    # top10统计
    top10_tags = []
    top10_tags_values = []
    for i in tags_list[:10]:
        top10_tags.append(i[0])
        top10_tags_values.append(i[1])

    return render(request, 'blog/about.html', locals())


def search(request):
    """
    搜索
    """
    key = request.GET['key']
    page_number = get_page(request)
    blog_count = Article.objects.filter(title__icontains=key).count()
    page_info = PageInfo(page_number, blog_count)
    _blog_list = Article.objects.filter(title__icontains=key)[page_info.index_start: page_info.index_end]
    return render(request, 'blog/search.html', {"blog_list": _blog_list, "pages": page_info, "key": key})


@login_required
def get_comment(request, pk):
    """
    发表评论
    """
    blog = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META.get("HTTP_X_FORWARDED_FOR")
            else:
                ip = request.META.get("REMOTE_ADDR")
            comment.request_ip = ip
            try:
                comment.request_address = get_req_info(ip)
            except Exception:
                pass
            comment.title = blog.title
            comment.email = request.user.email
            comment.url = str(request.headers['Referer'])  # 文章跳转url
            if '*' in DFAFilter().check_comments(comment.comment):  # 评论内容
                messages.error(request, '评论内容不合规，请修改后重新提交')
                return redirect('blog:get_comment', pk=pk)
            if '*' in DFAFilter().check_comments(request.user.username):  # user_name
                comment.user_name = '信球'
            else:
                comment.user_name = request.user.username
            comment.avatar_address = User.objects.get(id=request.user.pk).userinfo.avatar  # 头像链接转存
            comment.post = blog  # 关联评论与文章
            comment.user = request.user  # 关联评论与用户
            comment.save()
            blog.commenced(blog.post.all().count())
            return redirect('blog:get_comment', pk=pk)
    return redirect('blog:detail', pk=pk)


def subscription_record(request):
    """
    邮箱订阅
    """
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                _email = Subscription.objects.filter(Q(email=email))
                if _email:
                    messages.success(request, '此邮箱已经订阅过啦')
                    return redirect('blog:subscription_record')
                else:
                    sub = form.save(commit=False)
                    sub.save()
                    return redirect('blog:subscription_record')
            except ValueError:
                messages.error(request, '订阅失败')
    messages.success(request, '订阅成功，发布新文章后会通过邮箱及时通知你哟')
    return redirect('/blog')


def begin_unsub(request):
    """
    取消订阅跳转
    """
    return redirect('blog:unsubscribe')


def unsubscribe(request):
    """
    取消邮箱订阅
    """
    if request.method == 'POST':
        form = UnSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                _email = Subscription.objects.filter(Q(email=email))
                if not _email:
                    messages.error(request, '此邮箱还没有订阅')
                    return redirect('blog:unsubscribe')
                else:
                    Subscription.objects.filter(email=email).delete()
                    messages.success(request, '取消订阅成功')
                    return redirect('blog:unsubscribe')
            except ValueError:
                messages.error(request, '取消订阅失败')
    else:
        form = UnSubscriptionForm()
    return render(request, 'blog/unsub_email.html', locals())


@receiver(post_save, sender=Article)
def send_stu_email(sender, created, **kwargs):
    """
    文章发布监听器，发布文章时触发并直接发送邮件订阅通知
    """
    if created:
        blog = Article.objects.filter()
        if blog:
            link_id = Article.objects.all().order_by('-id').first().pk
            title = blog.values('title').first().get('title').strip()
            # 文章链接
            # 本地调试时请将 settings.website_author_link 换成 http://127.0.0.1:端口号
            link = settings.website_author_link + f'/blog/detail/{link_id}'
            _email = Subscription.objects.filter().values_list('email', flat=True)
            if _email:
                email_list = _email[:99999999]
                email_title = "文章订阅推送"
                email_body = "你订阅的 %s: %s 的博客发布新文章啦，快点击链接查阅吧\n文章：%s\n链接：%s" \
                             % (settings.website_author, settings.website_author_link, title, link)
                try:
                    send_mail(email_title, email_body, settings.EMAIL_HOST_USER, email_list,
                              auth_user=settings.EMAIL_HOST_USER,
                              auth_password=settings.EMAIL_HOST_PASSWORD)
                except Exception:
                    # 发送失败默认不发送，不影响发布文章
                    pass


def page_not_found_error(request, exception):
    return render(request, "404.html", status=404)


def page_error(request):
    return render(request, "404.html", status=500)
