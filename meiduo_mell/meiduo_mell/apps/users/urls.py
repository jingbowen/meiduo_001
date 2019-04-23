from django.conf.urls import url, include
from django.contrib import admin
from .views import RegisterView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', RegisterView.as_view(), name='register'),

]