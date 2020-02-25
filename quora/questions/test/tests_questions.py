from django.urls import reverse
from mixer.backend.django import mixer
import pytest

from questions.models import Question, Answer


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def some_user(api_client):
    user = mixer.blend('profiles.Profile')
    # api_client.force_login(user)
    return user


@pytest.fixture
def some_other_user():
    user = mixer.blend('profiles.Profile')
    return user


@pytest.fixture
def ask_question(some_user, client):
    return mixer.blend('questions.Question', author=some_user)


@pytest.fixture
def add_answer(some_user, client, ask_question):
    return mixer.blend('questions.Answer', author=some_user, question=ask_question)


@pytest.mark.django_db
def test_authorized_user_can_ask_question(some_user, api_client):
    api_client.force_login(some_user)
    question_data = {
        'content': 'test_content'
    }
    response = api_client.post(reverse('question-list'), data=question_data)

    assert Question.objects.all().count() == 1
    assert response.status_code == 201


@pytest.mark.django_db
def test_authorized_user_can_edit_question(some_user, api_client, ask_question):
    api_client.force_login(some_user)
    question_data = {
        'content': 'test_content-edited'
    }
    question_slug = Question.objects.first().slug
    response = api_client.put(
        reverse('question-detail', kwargs={'slug': question_slug}),
        data=question_data, )

    assert Question.objects.first().content == question_data['content']
    assert response.status_code == 200


@pytest.mark.django_db
def test_non_author_user_can_not_edit_question(some_other_user, api_client, ask_question):
    api_client.force_login(some_other_user)
    question_data = {
        'content': 'test_content-edited'
    }
    question_slug = Question.objects.first().slug
    response = api_client.put(
        reverse('question-detail', kwargs={'slug': question_slug}),
        data=question_data, )

    assert response.status_code == 403


@pytest.mark.django_db
def test_authorized_user_can_add_answer(some_user, api_client, ask_question):
    api_client.force_login(some_user)
    answer = {
        'content': 'test_content'
    }
    question_slug = Question.objects.first().slug
    response = api_client.post(
        reverse('answer-create', kwargs={'slug': question_slug}),
        data=answer, )

    assert Question.objects.first().answers.count() == 1
    assert response.status_code == 201


@pytest.mark.django_db
def test_authorized_user_can_add_only_one_answer(some_user, api_client, ask_question, add_answer):
    api_client.force_login(some_user)
    answer = {
        'content': 'test_content'
    }
    question_slug = Question.objects.first().slug
    response = api_client.post(
        reverse('answer-create', kwargs={'slug': question_slug}),
        data=answer, )

    assert Question.objects.first().answers.count() == 1
    assert response.status_code == 400
    assert response.json() == ['You have already answered that question']


@pytest.mark.django_db
def test_authorized_user_can_like_answer(some_other_user, api_client, ask_question, add_answer):
    api_client.force_login(some_other_user)
    response = api_client.post(
        reverse('answer-like', kwargs={'pk': add_answer.pk}))

    assert Answer.objects.first().voters.count() == 1
    assert response.status_code == 200


@pytest.mark.django_db
def test_authorized_user_can_unlike_answer(some_other_user, api_client, ask_question, add_answer):
    api_client.force_login(some_other_user)
    api_client.post(reverse('answer-like', kwargs={'pk': add_answer.pk}))
    response = api_client.delete(
        reverse('answer-like', kwargs={'pk': add_answer.pk}))

    assert Answer.objects.first().voters.count() == 0
    assert response.status_code == 200




@pytest.mark.django_db
def test_authorized_user_can_edit_answer(some_user, api_client, ask_question, add_answer):
    api_client.force_login(some_user)
    question_data = {
        'content': 'test_content-edited'
    }
    response = api_client.put(
        reverse('list-question-detail', kwargs={'pk': add_answer.pk}),
        data=question_data, )

    assert Answer.objects.first().content == question_data['content']
    assert response.status_code == 200


@pytest.mark.django_db
def test_non_author_user_can_not_edit_answer(some_other_user, api_client, ask_question, add_answer):
    api_client.force_login(some_other_user)
    question_data = {
        'content': 'test_content-edited'
    }
    response = api_client.put(
        reverse('list-question-detail', kwargs={'pk': add_answer.pk}),
        data=question_data, )

    assert response.status_code == 403
