
from .import settings

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models


class AliyunSms:
    def __init__(self):
        self.access_key_id = settings.ACCESS_KEY_ID
        self.access_key_secret = settings.ACCESS_KEY_SECRET
        self.sign_name = settings.SIGN_NAME
        self.template_code = settings.TEMPLATE_CODE

    def create_client(self):
        config = open_api_models.Config(access_key_id=self.access_key_id,
                                        access_key_secret=self.access_key_secret)
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    def send_sms(self, mobile, sms_code):
        client = self.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=mobile,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param="{'code':'%s'}" % sms_code
        )
        # 复制代码运行请自行打印 API 的返回值
        client.send_sms(send_sms_request)

    async def send_sms_async(self, mobile, sms_code):
        client = AliyunSms.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=mobile,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param="{'code':'%s'}" % sms_code
        )
        # 复制代码运行请自行打印 API 的返回值
        await client.send_sms_async(send_sms_request)




