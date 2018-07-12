import datetime
from django.utils import timezone
from django.shortcuts import render,redirect
from read_statistics.utils import seven_read,hot_blog_today,hot_blog_yesterday
from django.contrib.contenttypes.models import  ContentType
from blog.models import Blog
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm,RegForm


def getdayshot(somedays):
    today = timezone.now().date()
    dates = today - datetime.timedelta(days=somedays)
    blogs = Blog.objects \
                .filter(readdetails__date__lte=today,readdetails__date__gt=dates) \
                .values("id","title") \
                .annotate(readnum_sum=Sum("readdetails__read_num")) \
                .order_by("-readnum_sum")
    return blogs[:7]


def index(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    readnums,dates = seven_read(blog_content_type)
    todayhot = hot_blog_today(blog_content_type)
    yesterdayhot = hot_blog_yesterday(blog_content_type)

    if cache.get('sevenhot') is None:
        cache.set('sevenhot',getdayshot(7),3600)

    if cache.get('thirtyhot') is None:
        cache.set('thirtyhot',getdayshot(30),3600)

    context={}
    context['readnums'] = readnums
    context['dates'] = dates
    context['todayhot'] = todayhot
    context['yesterdayhot'] = yesterdayhot
    context['sevenhot'] = getdayshot(7)
    context['thirtyhot'] = getdayshot(30)
    return render(request,'index.html',context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.clean()['user']
            auth.login(request,user)
            return redirect(request.GET.get('from'))
    else:
        login_form = LoginForm()

    context={}
    context['login_form'] = login_form
    return render(request,'login.html',context)

def register(request):
    if request.method == 'POST':
        regform = RegForm(request.POST)
        if regform.is_valid():
            username = regform.cleaned_data['username']
            password = regform.cleaned_data['password']
            email = regform.cleaned_data['email']
            user = User.objects.create_user(username,email,password)
            user.save()
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from'),reverse('home'))
    else:
        regform = RegForm()
    context={}
    context['regform'] = regform
    return render(request,'register.html',context)