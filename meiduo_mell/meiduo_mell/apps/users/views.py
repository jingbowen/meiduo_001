from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,HttpResponseForbidden,JsonResponse
import re
from .models import User
from django.db import DatabaseError
from django.contrib.auth import login
from meiduo_mell.utils.response_code import RETCODE

# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        mobile = request.POST.get("mobile")
        sms_code = request.POST.get("sms_code")
        allow = request.POST.get("allow")
        if not all([username, password, password2, mobile, allow]):
            return HttpResponseForbidden("缺少必要的参数")
        if not re.match(r'^[A-Za-z0-9-_]{5,20}$', username):
            return HttpResponseForbidden("请输入5-20个字符的用户名")
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden("请输入8-20位的密码")
        if  password != password2:
            return HttpResponseForbidden("两次输入的密码不相等")
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('请输入正确的手机号码')
        if allow != "on":
            return HttpResponseForbidden('请勾选用户协议')
        # 手机验证码 pass
        try:
            User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})
        # login(request, username)

        return redirect("/")


class UserNameContView(View):
    def get(self,request,username,):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', "count": count})


class MobileCountView(View):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', "count": count})







