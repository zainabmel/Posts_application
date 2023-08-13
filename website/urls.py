from django.urls import path 
from . import views
#"." means "All"
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name='index'),#name may be index.html
    path('register', views.register,name='register'),
    path('login', views.login,name='login'),
    path('logout', views.logout,name='logout'),
    path('post', views.post,name='post'),
    path('allposts', views.allposts,name='allposts'),
    path('G_post', views.G_post,name='G_post'),
    path('U_post', views.U_post,name='U_post'),
    path('D_post', views.D_post,name='D_post')

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
