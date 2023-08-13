from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
#"." means "All"
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('posts/', views.post_list,name='post_list'),
    path('posts/<int:postID>/<int:authorID>', views.post_detail,name='post_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns) # to get the data as json from the url using .json
