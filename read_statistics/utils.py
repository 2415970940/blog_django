from .models import Readnum
from django.contrib.contenttypes.models import ContentType
from django.db.models import F

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read"%(ct.model,obj.pk)
    if not request.COOKIES.get(key):

        if Readnum.objects.filter(content_type=ct,object_id=obj.pk).count():
            readnum=Readnum.objects.filter(content_type=ct,object_id=obj.pk)
        else:
            readnum=Readnum.objects.create(content_type=ct,object_id=obj.pk)
        readnum.read_num+=1
        readnum.save()
        # readnum.update(read_num=F('read_num')+1)

    return key