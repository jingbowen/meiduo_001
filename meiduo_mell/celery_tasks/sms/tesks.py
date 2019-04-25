from celery_tasks.main import celery_app


# @celery_app.tesks() # 将下面的函数装饰成为celery任务
# def send_sms_code(mobile, sms_code):
#        （手机号，[随即生成的验证码，允许存在时间]，模板编号）
#     CCP().send_template_sms(mobile,[sms_code, 5], 1)

