import pytest
from fastapi import status

from db.models import User
from schemas.user_schema import UserRegisterSchema


def test_register_user(client):
    user_data = {
        'username': 'username',
        'password': 'password',
        'email': 'email@email.email',
        'first_name': 'first name',
        'last_name': 'last name',
    }
    response = client.post('/user/', json=user_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_login(client):
    user_data = {
        'username': 'username1',
        'password': 'password1',
        'email': 'email1@email.email',
        'first_name': 'first name',
        'last_name': 'last name',
    }
    response = client.post('/user/', json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    login_data = {
        'username': 'username1',
        'password': 'password1',
    }
    response = client.post('/user/token', json=login_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['access_token']
    assert response.json()['refresh_token']


def test_refresh_tokens_with_invalid_token(client):
    refresh_tokens_data = {
        'refresh_token': 'some invalid token'
    }
    response = client.post('/user/token/refresh', json=refresh_tokens_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_all_users(client):
    response = client.get('/user/')
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_retrieve_user_with_wrong_id(client, user):
    response = client.get(f'/user/{user.id}')
    assert response.status_code == status.HTTP_200_OK
