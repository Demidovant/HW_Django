from django.contrib import admin
from django.urls import path

from measurement.views import SensorsView, OneSensorView, MeasurmentView, IndexView, SensorsDetailsView

urlpatterns = [
    path('', IndexView),
    path('admin/', admin.site.urls),
    path('sensors/', SensorsView.as_view()),
    path('sensorsdetails/', SensorsDetailsView.as_view(), name='sensorsdetails'),
    path('sensors/<pk>/', OneSensorView.as_view()),
    path('measurement/', MeasurmentView.as_view()),
]
