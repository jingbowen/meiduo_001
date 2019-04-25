from celery import Celery
# 创建势力对象（生产者）
celery_app = Celery("note")
# 指定任务存放位子（经济人）
celery_app.config_from_object("celery_tasks.config")
# 注册执行的任务
celery_app.AsyncResult([celery_app.sms])