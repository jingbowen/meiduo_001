from django.conf.urls import url
from .views import ImageCodeView, SMSCodeView


urlpatterns = [
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', ImageCodeView.as_view(), name="image_code"),
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', SMSCodeView.as_view(), name="sms_code")
]