from QQLoginTool.QQtool import OAuthQQ
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework_jwt.settings import api_settings

from .models import OAuthQQUser
from .serializers import QQAuthUserSerializer

from cymall.utils.signature import Signature
from users.serializers import UserDetailSerializer


class QQAuthURLView(APIView):
    """提供qq登陆url"""

    def get(self, request):
        netx = request.query_params.get('next', '/')

        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state=netx)

        login_url = oauth.get_qq_url()
        return Response({'qq_login_url': login_url})


class QQAuthUserView(GenericAPIView):
    """QQ登陆回调"""
    serializer_class = QQAuthUserSerializer

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
        )

        # 获取openid
        try:
            access_token = oauth.get_access_token(code)
            openid = oauth.get_open_id(access_token)
        except Exception:
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 使用openid查询该QQ用户是否绑定过用户

        # openid = '1281726A823DE6F8E5BAACF3C7FA6493'
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:

            # 如果openid没绑定用户，返回加密openid给前端暂存，随注册表单一同发给后段创建新用户
            access_token_openid = Signature(300).encrypted_fields(data=openid)
            return Response({'access_token': access_token_openid})


        else:
            # 如果openid已绑定用户，直接生成JWT token，并返回
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            # 获取oauth_user关联的user
            user = oauth_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            serializer = UserDetailSerializer(user)
            data = serializer.data
            data['token'] = token
            return Response(data)

    def post(self, request):
        """openid绑定到用户"""

        # 获取序列化器对象
        serializer = self.get_serializer(data=request.data)
        # 开启校验
        serializer.is_valid(raise_exception=True)
        # 保存校验结果，并接收/ 返回创建用户
        user = serializer.save()

        # 生成JWT token，并响应
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        serializer = UserDetailSerializer(user)
        data = serializer.data
        data['token'] = token
        return Response(data)
