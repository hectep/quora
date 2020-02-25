from django.urls import reverse
import pytest

from profiles.models import Profile


@pytest.mark.django_db
def test_registration(client):
    credentials = {
        'username': 'test_user_test',
        'email': 'test_test@user.com',
        'password1': 'sometestpasswordQ1',
        'password2': 'sometestpasswordQ1',
    }
    response = client.post(reverse('django_registration_register'), data=credentials)

    assert response.status_code == 302
    assert Profile.objects.all().count() == 1


@pytest.mark.django_db
def test_rest_registration(client):
    credentials = {
        'username': 'test_user',
        'email': 'test@user.com',
        'password1': 'sometestpasswordQ1',
        'password2': 'sometestpasswordQ1',
    }
    response = client.post(reverse('rest_register'), data=credentials)

    assert response.status_code == 201
    assert Profile.objects.all().count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, password, is_authenticated', [
        ('testuser', 'testpassword', True),
        ('testuser', 'badpassword', False),
        ('baduser', 'testpassword', False),
        ('testuser', '', False),
        ('', 'testpassword', False),
    ]
)
def test_login(client, username, password, is_authenticated):
    data={
        'username': 'testuser',
        'password': 'testpassword'
    }
    user = Profile.objects.create_user(**data)
    response = client.post(reverse('login'), data={
        'username': username,
        'password': password
    }, follow=True)
    assert response.context['user'].is_authenticated == is_authenticated


def test_anonymous_user_cant_access_website(client):
    response = client.get(reverse('question-list'))

    assert response.status_code == 401
