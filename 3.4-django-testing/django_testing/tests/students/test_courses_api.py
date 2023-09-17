import pytest
from model_bakery import baker
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient
from students.models import Course, Student
from django.urls import reverse
import random
from django_testing import settings


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user('testuser')


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_courses(user, client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse("courses-list")
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == len(courses)


@pytest.mark.django_db
def test_get_one_course(user, client, course_factory):
    courses = course_factory(_quantity=10)
    index = random.randint(0, 9)
    course_id = courses[index].pk
    course_name = courses[index].name
    url = reverse('courses-detail', args=[course_id])
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['name'] == course_name


@pytest.mark.django_db
def test_get_filter_courses_by_id(user, client, course_factory):
    courses = course_factory(_quantity=10)
    index = random.randint(0, 9)
    course_id = courses[index].pk
    course_name = courses[index].name
    url = reverse("courses-list")
    filter_data = {'id': course_id}
    response = client.get(url, filter_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data[0]['name'] == course_name


@pytest.mark.django_db
def test_get_filter_courses_by_name(user, client, course_factory):
    courses = course_factory(_quantity=10)
    index = random.randint(0, 9)
    course_id = courses[index].pk
    course_name = courses[index].name
    url = reverse("courses-list")
    filter_data = {'name': course_name}
    response = client.get(url, filter_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data[0]['id'] == course_id


@pytest.mark.django_db
def test_create_course(user, client):
    count = Course.objects.count()
    url = reverse("courses-list")
    data = {'name': 'test_course'}
    response = client.post(url, data=data)
    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    response_data = response.json()
    assert response_data['name'] == data['name']


@pytest.mark.django_db
def test_update_course(user, client, course_factory):
    courses = course_factory(_quantity=10)
    index = random.randint(0, 9)
    course_id = courses[index].pk
    update_data = {'pk': course_id, 'name': 'test_course_update_name'}
    url = reverse("courses-detail", args=[course_id])
    response = client.patch(url, data=update_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['name'] == update_data['name']


@pytest.mark.django_db
def test_delete_course(user, client, course_factory):
    courses = course_factory(_quantity=10)
    index = random.randint(0, 9)
    course_id = courses[index].pk
    url = reverse("courses-detail", args=[course_id])
    response = client.delete(url)
    assert response.status_code == 204
    response_after_delete = client.get(url)
    assert response_after_delete.status_code == 404


@pytest.fixture
def students_quantity():
    return settings.MAX_STUDENTS_PER_COURSE


@pytest.mark.parametrize(
    ['students_count'],
    (
            (20,),
            (21,),
            (1000,),
            (10,),
            (1,),
    )
)
@pytest.mark.django_db
def test_students_quantity(client, students_count, student_factory, students_quantity):
    student = student_factory(_quantity=1)
    students_list = [student[0].pk] * students_count
    url = reverse('courses-list')
    data = {
        'name': 'test_course',
        'students': students_list
    }
    response = client.post(url, data=data)
    if students_count > students_quantity:
        assert response.status_code == 400
    else:
        assert response.status_code == 201
