from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django_testing.settings import MAX_STUDENTS_PER_COURSE
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, students):
        if len(students) > MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f'Максимум {MAX_STUDENTS_PER_COURSE} студентов должно быть на курсе')
        return students
