from django.conf.urls import url
from .views import ImageCodeView


urlpatterns = [
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', ImageCodeView.as_view()),
]