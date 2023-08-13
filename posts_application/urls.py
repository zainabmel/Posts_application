from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('website.urls')),
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    path('posts/',include('posts.urls'))
]

urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)