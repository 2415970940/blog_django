import datetime
from django.utils import timezone
from django.shortcuts import render,redirect
from read_statistics.utils import seven_read,hot_blog_today,hot_blog_yesterday
from django.contrib.contenttypes.models import  ContentType
from blog.models import Blog
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth

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
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
       return render(request,'error.html',{'message':'用户或密码不正确'})