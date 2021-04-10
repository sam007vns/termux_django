from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.login,name="login"),
    path('click_photo/<str:cam_type>',views.click_photo,name="click_photo"),
    path('photos',views.photos,name="photos"),
    path('home',views.home,name="home"),
    path('torch/<str:value>',views.torch,name="torch"),
    path('logout',views.logout,name="logout"),
    path('location',views.get_location,name="location"),
    path('record_audio_now',views.record_audio_now,name="record_audio_now"),
    path('recordings',views.view_audio_records,name="recordings"),
    path('view_call_logs',views.view_call_logs,name="view_call_logs"),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)