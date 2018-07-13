from django.shortcuts import redirect,render
from django.urls import reverse
from .models import Comment
from  django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
from django.http import JsonResponse
# Create your views here.
def update_comment(request):
    refere=request.META.get('HTTP_REFERER',reverse('home'))
    comment_form = CommentForm(request.POST,user=request.user)
    data={}

    if comment_form.is_valid():
        comment = Comment()
        comment.text = comment_form.cleaned_data['text']
        comment.user = comment_form.cleaned_data['user']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        # 返回数据
        data['status']='SUCCESS'
        data['username']=comment.user.username
        data['comment_time']=comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text']=comment.text
    else:
        # return render(request,'error.html',{'message':comment_form.errors,'redirect_to':refere})
        data['status']='ERROR'
        data['messages']=list(comment_form.errors.values())[0][0]
    return JsonResponse(data)

