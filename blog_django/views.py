import datetime
from django.utils import timezone
from django.shortcuts import render_to_response
from read_statistics.utils import seven_read,hot_blog_today,hot_blog_yesterday
from django.contrib.contenttypes.models import  ContentType
from blog.models import Blog
from django.db.models import Sum

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

    context={}
    context['readnums'] = readnums
    context['dates'] = dates
    context['todayhot'] = todayhot
    context['yesterdayhot'] = yesterdayhot
    context['sevenhot'] = getdayshot(7)
    context['thirtyhot'] = getdayshot(30)
    return render_to_response('index.html',context)