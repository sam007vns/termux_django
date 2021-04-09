from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.login,name="login"),
    path('click_photo/<str:cam_type>',views.click_photo,name="click_photo"),
    path('photos',views.photos,name="photos"),
    path('home',views.home,name="home"),
    path('home/torch/<str:value>',views.home,name="home"),
    path('logout',views.logout,name="logout"),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)