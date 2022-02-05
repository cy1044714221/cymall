
from django.urls import path
from . import views

urlpatterns = [
    path('operationaldata/index', views.index),
    path('operationaldata/todays_data', views.todays_data),
    path('operationaldata/todays_charts', views.todays_charts),
    path('operationaldata/yesterday_data', views.yesterday_data),
    path('operationaldata/yesterday_charts', views.yesterday_charts),
    path('operationaldata/user_data', views.user_data),
    path('operationaldata/user_charts', views.user_charts),




]