from django.conf.urls import include, url
from .views import *

app_name = 'watermarker'

urlpatterns = [
    url('test', test_task),
    url('upload_video', upload_video),
    url('search_video', search_video),
    url('get_video', get_video),
    url('', index),
]
