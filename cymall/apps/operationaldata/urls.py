
from django.urls import path
from . import views

urlpatterns = [

    path('operationaldata/all_data', views.all_data),
    path('operationaldata/today_data', views.today_data),




]