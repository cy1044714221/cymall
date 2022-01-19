# 编辑异步任务
# from celery_tasks.aliyun_sms.aliyun_sms import AliyunSms
from celery_tasks.main import celery_app
from celery_tasks.aliyun_sms.aliyun_sms import AliyunSms


@celery_app.task(name='aliyun_send_sms_codes')
def aliyun_send_sms_codes(mobile, sms_code):
    """
    # 发送短信异步任务
    :param mobile:
    :param sms_code:
    """
    # AliyunSms().send_sms(mobile, sms_code)
    print('短信异步任务执行完毕')



