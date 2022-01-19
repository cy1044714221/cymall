from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    # api接口文档
    re_path(r'^docs', include_docs_urls(title='API')),
    # JWT签发
    re_path(r'^authorizations$', obtain_jwt_token),

    path('', include('users.urls')),  # 用户模块
    path('', include('verifications.urls'))  # 验证模块
]
