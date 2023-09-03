from django.shortcuts import redirect
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


def IndexView(request):
    """Класс перенаправляет с baseurl/api на baseusl/api/sensorsdetails"""
    return redirect('sensorsdetails')


class SensorsView(ListCreateAPIView):
    """Класс позволяет добавить датчик и получить список всех датчиков"""
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class OneSensorView(RetrieveUpdateAPIView):
    """Класс позволяет получить данные конкретного датчика с температурами"""
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurmentView(ListCreateAPIView):
    """Класс позволяет добавить измерение и получить список всех измерений"""
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class SensorsDetailsView(ListCreateAPIView):
    """Класс позволяет получить подробный список всех датчиков"""
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer