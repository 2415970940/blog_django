"""blog_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import blog_list,blog_detail,type_blog,blog_date

urlpatterns = [
    path('', blog_list,name="blog_list"),
    path('<int:blog_pk>',blog_detail,name="blog_detail" ),
    path('blogType/<int:blog_type_pk>',type_blog,name="type_blog" ),
    path('blog/<int:year>/<int:month>',blog_date,name="blog_date"),
]
