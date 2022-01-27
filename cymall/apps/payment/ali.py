from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig

# app_private_key_string = open("/path/to/your/private/key.pem").read()
# alipay_public_key_string = open("/path/to/alipay/public/key.pem").read()
#
# app_private_key_string == """
#     -----BEGIN RSA PRIVATE KEY-----
#     base64 encoded content
#     -----END RSA PRIVATE KEY-----
# """
#
# alipay_public_key_string == """
#     -----BEGIN PUBLIC KEY-----
#     base64 encoded content
#     -----END PUBLIC KEY-----
# """

alipay = AliPay(
            appid="2021000119604948",
            app_notify_url=None,  # 默认回调 url
            app_private_key_string='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzjMgnhgoGmhl66qyOpA+u1aOV0XTrqyy8P+g4uCON3fcR5v4JbotVyKzFrDBekO+z1qeo4JpXZIz9uxq8EA5SGp7+1JRHMICgsdIJfUyxvWUc7FME1wBOOTva4L495w8EhLG/QiX8vMi8W3diEKQaVbjABl6sQFDkumA2J9KJf8hq5ZALIvRagfcmC4GunWrJRKwsLsK4gcy5a9X97KYtq4qeGSYuFKpjfo3tYjr3ZirrDj+fw3UwcJWioU2h79tfE7lNWrxn3fTBlJKh/oUYpevPToT6LSlvNWvgVF2FPyj6x0Sghl07DiFUkrVnFhK5AyYT4gg4ToCGE3dGNZa7wIDAQAB',
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzjMgnhgoGmhl66qyOpA+u1aOV0XTrqyy8P+g4uCON3fcR5v4JbotVyKzFrDBekO+z1qeo4JpXZIz9uxq8EA5SGp7+1JRHMICgsdIJfUyxvWUc7FME1wBOOTva4L495w8EhLG/QiX8vMi8W3diEKQaVbjABl6sQFDkumA2J9KJf8hq5ZALIvRagfcmC4GunWrJRKwsLsK4gcy5a9X97KYtq4qeGSYuFKpjfo3tYjr3ZirrDj+fw3UwcJWioU2h79tfE7lNWrxn3fTBlJKh/oUYpevPToT6LSlvNWvgVF2FPyj6x0Sghl07DiFUkrVnFhK5AyYT4gg4ToCGE3dGNZa7wIDAQAB',
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True,  # 默认 False
            verbose=True,  # 输出调试数据
            config=AliPayConfig(timeout=15)  # 可选，请求超时时间
        )

order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="20161112",
    total_amount=0.01,
    subject='subject',
    return_url="https://example.com",
    notify_url="https://example.com/notify" # 可选，不填则使用默认 notify url
)