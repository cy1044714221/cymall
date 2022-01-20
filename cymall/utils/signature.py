# 加密解密工具
from itsdangerous import TimedJSONWebSignatureSerializer as TJWS, BadData
from django.conf import settings


class Signature:
    def __init__(self, time=300):
        self.time = time

    def encrypted_fields(self, data):
        tjws = TJWS(settings.SECRET_KEY, self.time)
        token = tjws.dumps(data)
        token = token.decode()
        return token

    def decryption_fields(self, token):
        twjs = TJWS(settings.SECRET_KEY, self.time)
        try:
            data = twjs.loads(token)
        except BadData:
            return None
        return data
