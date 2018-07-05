from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator
from .models import Blog,BlogType
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read


blogs_per_pages=5
# Create your views here.
def blog_comm_data(request,blog_list):
    paginator = Paginator(blog_list,blogs_per_pages)
    page_num = request.GET.get('page',1)
    page_blogs =paginator.get_page(page_num)

    current_page = page_blogs.number
    page_range =[x for x in range(current_page-2,current_page+3) if x>0 and x<=paginator.page_range[-1]]

    if page_range[0]-1>1:
        page_range.insert(0,"...")
    if paginator.num_pages-page_range[-1]>1:
        page_range.append("...")

    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # number of pre blog type
    blog_types = BlogType.objects.annotate(blog_count=Count("blog_blog"))
    # number of date_blog sort
    ds=Blog.objects.dates('create_time','month',order='ASC')[:10]
    ds_dict={}
    for blogdate in ds:
        num = Blog.objects.filter(create_time__year=blogdate.year,
                                  create_time__month=blogdate.month).count()
        ds_dict[blogdate]=num


    context = {}
    context['page_range']=page_range
    context['blogs']=page_blogs.object_list
    context['page_blogs']=page_blogs
    context['blog_types']=blog_types
    context['blog_dates']=ds_dict
    return context


def blog_list(request):
    blog_all = Blog.objects.all()
    context =blog_comm_data(request,blog_all)
    return render_to_response("blog/blog_list.html",context)

def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key=read_statistics_once_read(request,blog)
    context['blog']=blog
    context['pre_blog']=Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog']=Blog.objects.filter(create_time__lt=blog.create_time).first()


    response = render_to_response("blog/blog_detail.html",context)
    response.set_cookie(read_cookie_key,"true")
    return response

def type_blog(request,blog_type_pk):
    type_names= get_object_or_404(BlogType,pk =blog_type_pk )
    blog_all = Blog.objects.filter(blog_type=type_names)
    context=blog_comm_data(request,blog_all)
    context['blog_type']=type_names
    return render_to_response("blog/blog_type.html",context)

def blog_date(request,year,month):
    blog_all = Blog.objects.filter(create_time__year=year,create_time__month=month)
    content = blog_comm_data(request,blog_all)
    content['date']="%s年%s月"%(year,month)
    return render_to_response("blog/blog_date.html",content)