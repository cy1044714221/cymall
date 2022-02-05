from datetime import timedelta

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

import json

from django.shortcuts import render, redirect
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Geo, Grid
from django.utils import timezone
from users.models import User
from orders.models import OrderInfo
from users.models import Address

from areas.models import Area


def index(request):
    title = '标题222'
    legends = ['销量']
    tt = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    return render(request, 'operationaldata/index.html', locals())


# 校验用户登陆 / 是否有管理员权限
def Check_Login_isstaff(func):
    def warpper(request):
        if not request.user.is_staff and not request.user.is_authenticated:
            return redirect('admin/login/?next=%s' % request.path)
        else:
            return func(request)

    return warpper


# 此处 前后端分离应该写在一个函数中，否则查询两次， 后期优化修改  定义两个相同的变量名会导致数据一样
# 今日运营数据
today = timezone.now().date()  # 今日数据
or_qs = OrderInfo.objects.filter(create_date__gt=today).values_list('create_date', 'total_count', 'total_amount',
                                                                    'order_status')
df = pd.DataFrame(list(or_qs), columns=['create_date', 'total_count', 'total_amount', 'order_status'])
df['hours'] = df['create_date'].dt.strftime('%H')
s1 = df.groupby('hours').agg(total_count=('total_count', 'sum'), total_amount=('total_amount', 'sum'))


@Check_Login_isstaff
def todays_data(request):
    total_order_count = df['total_count'].sum()
    gmv = df['total_amount'].sum()
    user_count = User.objects.filter(date_joined__gt=today).count()
    print(locals())
    return render(request, 'operationaldata/todays_data.html', locals())


@Check_Login_isstaff
def todays_charts(request):
    todays_charts = (
        Bar()
            .add_xaxis([str(x) + '时' for x in s1.index.to_list()])
            .add_yaxis("销量", [x for x in s1.total_count.to_list()])
            .add_yaxis("销售额", [x for x in s1.total_amount.to_list()])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            title_opts=opts.TitleOpts(title="销量/销售额", subtitle="数据更新日期：" + timezone.now().__str__()),
            brush_opts=opts.BrushOpts(), )
            .dump_options_with_quotes()
    )
    return JsonResponse(json.loads(todays_charts))


# 昨日运营数据
yesterday = timezone.now().date() + timedelta(days=-1)  # 昨日数据
or_qs2 = OrderInfo.objects.filter(create_date__date=yesterday).values_list('create_date', 'total_count', 'total_amount',
                                                                           'order_status')
df2 = pd.DataFrame(list(or_qs2), columns=['create_date', 'total_count', 'total_amount', 'order_status'])
df2['hours'] = df2['create_date'].dt.strftime('%H')
s2 = df2.groupby('hours').agg(total_count=('total_count', 'sum'), total_amount=('total_amount', 'sum'))


@Check_Login_isstaff
def yesterday_data(request):
    total_order_count = df2['total_count'].sum()
    gmv = df2['total_amount'].sum()
    user_count = User.objects.filter(date_joined__gt=yesterday).count()
    return render(request, 'operationaldata/yesterday_data.html', locals())


@Check_Login_isstaff
def yesterday_charts(request):
    c = (
        Bar()
            .add_xaxis([str(x) + '时' for x in s2.index.to_list()])
            .add_yaxis("销量", [x for x in s2.total_count.to_list()])
            .add_yaxis("销售额", [x for x in s2.total_amount.to_list()])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            title_opts=opts.TitleOpts(title="销量/销售额", subtitle="数据更新日期：" + timezone.now().__str__()),
            brush_opts=opts.BrushOpts(), )
            .dump_options_with_quotes()
    )
    return JsonResponse(json.loads(c))


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


JsonResponse = json_response

# 用户数据图标 -------------------------------

order_qs = OrderInfo.objects.all().values_list('address', flat=True)
order_qs = list(order_qs)
address_qs = Address.objects.filter(id__in=order_qs).values_list('province', flat=True)
df3 = pd.DataFrame(list(address_qs), columns=['id'])

# 取出地址 转为 dataframe
areas = Area.objects.filter(parent=None).values_list('id', 'name')
areas_df = pd.DataFrame(list(areas), columns=['id', 'name'])

df4 = pd.merge(df3, areas_df, how='inner')

s4 = df4.groupby('name').agg(sales=('name','count')).reset_index()



def user_data(request):
    """ 总用户数量。。。。。"""
    return render(request, 'operationaldata/user_data.html')


from pyecharts.faker import Faker

def user_charts(request):
    bar = (
        Bar()
            .add_xaxis([x for x in s4.name.to_list()])
            .add_yaxis("销量", [list(x) for x in s4.values])
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90)),
            legend_opts=opts.LegendOpts(pos_left="40%"),
        )
    )

    geo = (
        Geo(is_ignore_nonexistent_coord=True)
            .add_schema(maptype="china")
            .add("地图分布", [list(z) for z in s4.values])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="用户消费地区分布", subtitle="数据更新日期：" + timezone.now().__str__()),
        )
    )
    grid = (
        Grid()
            .add(bar, grid_opts=opts.GridOpts(pos_top="70%", pos_right="65%"))
            .add(geo, grid_opts=opts.GridOpts(pos_left="70%"))
            .dump_options_with_quotes()
    )

    return JsonResponse(json.loads(grid))
