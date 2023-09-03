from rest_framework import serializers

from measurement.models import Sensor, Measurement

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class MeasurementSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=True, allow_null=True)
    class Meta:
        model = Measurement
        fields = ['sensor_id', 'temperature', 'created_at', 'image']


class MeasureSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=True, allow_null=True)
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at', 'image']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasureSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
