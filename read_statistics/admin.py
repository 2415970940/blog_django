from django.contrib import admin
from .models import Readnum
# Register your models here.
@admin.register(Readnum)
class ReadnumAdmin(admin.ModelAdmin):
    list_display=('read_num','content_object')