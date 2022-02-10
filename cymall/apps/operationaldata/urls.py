
from django.urls import path
from . import views

urlpatterns = [
    path('operationaldata/dt_data/<dt>', views.dt_data),
    path('operationaldata/dt_charts/<dt>', views.dt_charts),
    path('operationaldata/user_data', views.user_data),
    path('operationaldata/user_charts', views.user_charts),

]
