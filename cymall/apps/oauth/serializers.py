from django_redis import get_redis_connection
from rest_framework import serializers

from users.models import User
from oauth.models import OAuthQQUser
from cymall.utils.signature import Signature


class QQAuthUserSerializer(serializers.Serializer):
    """QQ登录创建用户序列化器"""
    access_token = serializers.CharField(label='操作凭证')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码')

    def validate(self, attrs):
        # 检验access_token
        access_token = attrs['access_token']
        # 获取身份凭证
        openid = Signature(300).decryption_fields(token=access_token)
        if not openid:
            raise serializers.ValidationError('无效的access_token')

        attrs['openid'] = openid

        # 检验短信验证码
        mobile = attrs['mobile']
        sms_code = attrs['sms_code']
        redis_conn = get_redis_connection('sms_codes')
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证码错误')

        # 如果用户存在，检查用户密码
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            pass
        else:
            password = attrs['password']
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')

            attrs['user'] = user
        return attrs

    def create(self, validated_data):
        # 获取校验的用户
        user = validated_data.get('user')

        if not user:
            # 用户不存在,新建用户
            user = User.objects.create_user(
                username=validated_data['mobile'],
                password=validated_data['password'],
                mobile=validated_data['mobile'],
            )

        # 将用户绑定openid
        OAuthQQUser.objects.create(
            openid=validated_data['openid'],
            user=user
        )
        # 返回用户数据
        return user
