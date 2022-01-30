"""cymall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', include('operationaldata.urls')),  # 自定义后台数据
    path('admin/doc/', include('django.contrib.admindocs.urls')),  # Django 管理文档生成器
    path('admin/', admin.site.urls),

    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # re_path(r'^docs/', include_docs_urls(title='API文档')),
    re_path(r'^', include_docs_urls(title='API文档')),

    # JWT签发
    re_path(r'^authorizations$', obtain_jwt_token),

    path('', include('users.urls')),

    path('oauth/', include('oauth.urls')),

    path('', include('verifications.urls')),  # 短信验证
    path('', include('areas.urls')),  # 区域
    path('', include('carts.urls')),  # 购物车
    path('', include('orders.urls')),  # 订单
    path('', include('payment.urls')),  # 支付

]
