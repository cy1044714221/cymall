import re
from rest_framework import serializers
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings
from celery_tasks.email.tasks import send_verify_email
from cymall.utils.signature import Signature
from .models import User, Address


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True, help_text="测试填写: 123456 ", )
    allow = serializers.CharField(label='同意协议', write_only=True, help_text="测试填写: true ", )
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow', 'token']

        extra_kwargs = {
            'username': {
                'min_length': 4,
                'max_length': 20,
                "help_text": "必填；长度为5-20个字符；只能包含字母、数字、特殊字符“@”、“.”、“-”和“_”。",
                'error_messages': {
                    'min_length': '用户名仅限4-20个字符',
                    'max_length': '用户名仅限4-20个字符',
                }
            },
            'password': {
                'min_length': 8,
                'max_length': 40,
                'write_only': True,
                "help_text": "必填；长度为8-40个字符。",
                'error_messages': {
                    'min_length': '密码仅限4-20个字符',
                    'max_length': '密码仅限4-20个字符',
                }
            },
        }

    def validate(self, attrs):

        """校验手机号码"""
        if not re.match(r'1[3-9]\d{9}$', attrs['mobile']):
            raise serializers.ValidationError('手机号码格式错误')

        """校验两次密码"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')

        """校验短信验证码"""
        redis_conn = get_redis_connection('sms_codes')
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code is None:
            raise serializers.ValidationError('短信验证码无效')
        if attrs['sms_code'] != real_sms_code.decode():  # 验证码从redis取出需要解码, 如果为空不能decode()
            raise serializers.ValidationError('验证码错误')

        """校验同意协议"""
        if attrs['allow'] != 'true':
            raise serializers.ValidationError('请同意用户注册协议')

        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # 手动签发JWT
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用函数，生成payload
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 引用函数，生成JWT

        payload = jwt_payload_handler(user)  # 根据user生成载荷
        token = jwt_encode_handler(payload)  # 传入载荷 生成完整的JW
        user.token = token  # 给前端发挥信息时候增加jwt token

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'email_active', 'token']


class EmailSerializer(serializers.ModelSerializer):
    """更新验证邮箱"""

    class Meta:
        model = User
        fields = ['id', 'email']
        extra_kwargs = {
            'email': {
                'required': True
            },
        }

    def update(self, instance, validated_data):
        """重写方法， 增加发送邮件"""
        instance.email = validated_data.get('email')
        instance.save()

        # 增加校验邮箱
        data = {'id': instance.id, 'email': instance.email}
        token = Signature(300).encrypted_fields(data)

        # 生成邮箱激活链接
        verify_email_url = '127.0.0.1:8000/email_verify_url?token=' + token
        send_verify_email.delay(instance.email, verify_url=verify_email_url)

        return instance


class AddressSerializer(serializers.ModelSerializer):
    # 省市区 和 对应ID
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)

    class Meta:
        model = Address
        # " id -user addressee province city district place mobile -is_deleted -create_date -update_date"
        fields = ['id', 'addressee', 'province', 'city', 'district', 'province_id', 'city_id', 'district_id', 'place',
                  'mobile']

    def validate_mobile(self, value):
        """
        验证手机号
        """
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        # 如果地址存在 返回原来到地址， 如果不存在 新建
        try:
            address_a = Address.objects.get(**validated_data)
        except:
            address_a = None
        if address_a:
            address = address_a
        else:
            address = super().create(validated_data)
        return address
