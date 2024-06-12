from django.contrib import admin
from django.urls import path
from downloader.views import download_video_view, download_complete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', download_video_view, name='download_video'),
    path('complete/', download_complete, name='download_complete'),
]
