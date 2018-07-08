from django.shortcuts import render_to_response
from read_statistics.utils import seven_read
from django.contrib.contenttypes.models import  ContentType
from blog.models import Blog

def index(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    readnums,dates = seven_read(blog_content_type)
    context={}
    context['readnums'] = readnums
    context['dates'] = dates
    return render_to_response('index.html',context)