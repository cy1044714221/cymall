import re

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True, help_text="测试填写: 123456 ", )
    allow = serializers.CharField(label='同意协议', write_only=True, help_text="测试填写: true ", )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'sms_code', 'phone_num', 'allow']

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
        if not re.match(r'1[3-9]\d{9}$', attrs['phone_num']):
            raise serializers.ValidationError('手机号码格式错误')
        """校验两次密码"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')
        """校验短信验证码"""

        """校验同意协议"""
        if attrs['allow'] != 'true':
            raise serializers.ValidationError('请同意用户注册协议')

        return attrs

    def create(self, validated_data):
        # 校验ok之后删除不需要写入数据库的参数
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
