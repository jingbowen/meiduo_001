from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,HttpResponseForbidden,JsonResponse
import re
from .models import User
from django.db import DatabaseError
from django.contrib.auth import login,authenticate
from meiduo_mell.utils.response_code import RETCODE
from django_redis import get_redis_connection


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
        image_code = request.POST.get("image_code")
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
        redis_conn = get_redis_connection("verify_code")
        sms_code_server = redis_conn.get("sms_%s" % mobile)
        if sms_code_server is None:
            return render(request, "register.html", {"sms_code_errmsg": "验证码无效"})
        if sms_code != sms_code_server.decode():
            return render(request, "register.html",{"sms_code_errmsg": "验证码错误"})

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


class LoginView(View):
    def get(self,request):
        return render(request,"login.html")

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        remembered = request.POST.get("remembered")
        if all([username, password]) is None:
            return HttpResponseForbidden("缺少必传的参数")
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden('请输入正确的用户名或手机号')

            # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('密码最少8位，最长20位')

        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, "login.html", {"account_errmsg":"用户名或密码错误"})
        login(request, user)
        if remembered != "on":
            request.session.set_expiry(0)
        return redirect("/")















