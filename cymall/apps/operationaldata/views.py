from django.shortcuts import render


# Create your views here.
from users.models import User
from goods.models import Goods
from orders.models import OrderInfo


def stateboard(request):
    user_count = User.objects.count()
    goods_count = Goods.objects.count()
    orders_count = OrderInfo.objects.count()
    return render(request, "operationaldata/stateboard.html", locals())
