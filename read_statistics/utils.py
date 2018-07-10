import datetime
from .models import Readnum,ReadDetail
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.utils import timezone

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read"%(ct.model,obj.pk)
    if not request.COOKIES.get(key):
        readnum,created =Readnum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readnum.read_num+=1
        readnum.save()
        # readnum.update(read_num=F('read_num')+1)

        today = timezone.now().date()
        readdetail,created=ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=today)
        readdetail.read_num+=1
        readdetail.save()
    return key

def seven_read(contenttype):
    today = timezone.now().date()
    read_num=[]
    dates = []
    for i in range(6,-1,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime("%m/%d"))
        readdetail = ReadDetail.objects.filter(content_type=contenttype,date=date)
        result = readdetail.aggregate(read_sum = Sum('read_num'))
        read_num.append(result['read_sum'] or 0)
    return read_num,dates

def hot_blog_today(contenttype):
    today = timezone.now().date()
    readdetail = ReadDetail.objects.filter(content_type=contenttype,date=today).order_by("-read_num")
    return readdetail[:7]

def hot_blog_yesterday(contenttype):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    readdetail = ReadDetail.objects.filter(content_type=contenttype,date=yesterday).order_by("-read_num")
    return readdetail[:7]