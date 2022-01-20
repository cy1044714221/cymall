# 邮件发送参数
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True  # QQ邮箱需要配置此项
# 发送邮件的邮箱
EMAIL_HOST_USER = '1044714221@qq.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'svssrerjpwrbbbgb'
# 收件人看到的发件人
EMAIL_FROM = '<1044714221@qq.com>'  # QQ邮箱不让修改from头，