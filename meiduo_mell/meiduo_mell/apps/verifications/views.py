
from django.http import HttpResponse, JsonResponse
from django.views import View
from django_redis import get_redis_connection
from meiduo_mell.utils.response_code import RETCODE
from meiduo_mell.libs.captcha.captcha import captcha
import random


# Create your views here.


class ImageCodeView(View):
    def get(self, request, uuid):
        name, text, image = captcha.generate_captcha()

        # 保存图片验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, 300, text)
        # 响应图片验证码
        return HttpResponse(image, content_type='image/jpg')


class SMSCodeView(View):
    def get(self, request, mobile):
        image_code_client = request.GET.get("image_code")
        uuid = request.GET.get("uuid")
        redis_conn = get_redis_connection("verify_code")
        sms_flag = redis_conn.get("sms_flag_%s" % mobile)
        if sms_flag:
            return JsonResponse({'code': RETCODE.THROTTLINGERR, "errmsg": "频繁发送短信"})

        if not all([image_code_client, uuid]):
            return JsonResponse({"code":RETCODE.NECESSARYPARAMERR,"errmsg":"缺少必传的参数"})
        redis_conn = get_redis_connection("verify_code")
        image_code_server = redis_conn.get("img_%s" % uuid)
        redis_conn.delete("img_%s" % uuid)
        if image_code_server is None:
            return JsonResponse({"code": RETCODE.IMAGECODEERR, "errmsg": "验证码失效"})
        image_code_server = image_code_server.decode()
        if image_code_server.lower() != image_code_client.lower():
            return JsonResponse({'code': RETCODE.IMAGECODEERR, "errmsg": "输入的验证码有误"})
        sms_code = "%06d" % random.randint(0, 999999)
        print(sms_code)
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, 300, sms_code)
        pl.setex("sms_flag_%s" % mobile, 60, 1)
        pl.execute()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})





