from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import ReadnumMethod,ReadDetail

# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model,ReadnumMethod):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING,related_name="blog_blog")
    content =RichTextUploadingField()
    #contenttype反取
    readdetails = GenericRelation(ReadDetail)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "blog:%s"%self.title

    class Meta:
        ordering=['-create_time']
