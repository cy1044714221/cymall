import random

from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from celery_tasks.aliyun_sms.tasks import aliyun_send_sms_codes


class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 判断手机号码60S内是否发送过短信
        redis_conn = get_redis_connection('sms_codes')
        if redis_conn.get('send_flag_%s' % mobile):  # 取到值代表此手机号码60S内发送过短信
            return Response({'message': '此手机号码频繁发送短信'}, status=status.HTTP_400_BAD_REQUEST)

        sms_code = '%06d' % random.randint(0, 999999)

        pl = redis_conn.pipeline()
        # 验证码存储到redis
        pl.setex('sms_%s' % mobile, 300, sms_code)
        # 存储验证码发送标记，60秒内是否重复发送
        pl.setex('send_flag_%s' % mobile, 60, 1)
        pl.execute()
        aliyun_send_sms_codes.delay(mobile, sms_code)

        return Response({'message': 'ok' + sms_code}, status=status.HTTP_202_ACCEPTED)
