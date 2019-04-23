from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,HttpResponseForbidden
import re
from .models import User

# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        mobile = request.POST.get("mobile")
        allow = request.POST.get("allow")
        if not all([username,password,password2,mobile,allow]):
            return HttpResponseForbidden("缺少必传的参数")
        if not re.match("^[a-zA-Z0-9-_]{5,20}",username):
            return HttpResponseForbidden('请输入5-20个字符的用户名')
        if password != password2:
            return HttpResponseForbidden('两次输入的密码不一致')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20位的密码')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('请输入正确的手机号码')
        if allow != 'on':
            return HttpResponseForbidden('请勾选用户协议')
        try:
            User.objects.create_user(username=username,password=password,mobile=mobile)
        except:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})
        return redirect("/index/")

