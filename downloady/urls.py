from django.contrib import admin
from django.urls import path
# from downloader.views import download_video_view, download_complete
from downloader.views import download_video_view, file_iterator

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', download_video_view, name='download_video'),
    # path('complete/', download_complete, name='download_complete'),
    path('complete/', file_iterator, name='download_complete'),
]
