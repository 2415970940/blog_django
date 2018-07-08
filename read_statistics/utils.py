from .models import Readnum,ReadDetail
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.utils import timezone

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read"%(ct.model,obj.pk)
    if not request.COOKIES.get(key):

        # if Readnum.objects.filter(content_type=ct,object_id=obj.pk).count():
        #     readnum=Readnum.objects.filter(content_type=ct,object_id=obj.pk)
        # else:
        #     readnum=Readnum.objects.create(content_type=ct,object_id=obj.pk)
        readnum,created =Readnum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readnum.read_num+=1
        readnum.save()
        # readnum.update(read_num=F('read_num')+1)

        today = timezone.now().date()
        # if ReadDetail.objects.filter(content_type=ct,object_id=obj.pk,date=today).count():
        #     readdetail=ReadDetail.objects.get(content_type=ct,object_id=obj.pk,date=today)
        # else:
        #     readdetail=ReadDetail.objects.create(content_type=ct,object_id=obj.pk,date=today)
        readdetail,created=ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=today)
        readdetail.read_num+=1
        readdetail.save()
    return key