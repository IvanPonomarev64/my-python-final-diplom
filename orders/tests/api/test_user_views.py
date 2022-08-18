import pytest
from model_bakery import baker

from .fixtures import URL, client, user_factory, confirm_email_token_factory
from rest_framework.authtoken.models import Token

from api.models import User, Contact


@pytest.mark.django_db
def test_create_user(client, user_factory):
    user_factory(_quantity=1)
    new_user = baker.prepare(User).__dict__

    assert new_user.pop('_state')
    new_user['password_2'] = new_user['password']

    assert new_user['password_2'] == new_user['password']
    count = User.objects.count()
    url = f"{URL}user/"
    resp = client.post(
        url,
        data=new_user
    )
    assert resp.status_code == 200
    assert User.objects.count() == count + 1
    assert resp.json()['response']
    response = resp.json()['response']
    assert response['status'] == '201'


@pytest.mark.django_db
def test_login_user(client, user_factory):
    user = user_factory(_quantity=1)[0]
    url = URL + 'login/'
    res = client.post(
        url,
        data={
            'email': user.email,
            'password': user.password
        }
    )
    assert res.status_code == 200
    assert res.json()['Status'] == True
    assert Token.objects.count() == 1


@pytest.mark.django_db
def test_update_user(client, user_factory):
    user = user_factory(_quantity=1)[0]
    url = f"{URL}user/{user.pk}/"
    client.force_authenticate(user=user)

    data = {
        'email': 'test@mail.com'
    }
    update_data = client.put(url, data=data).json()
    assert update_data['Status']

    get_user = client.get(url).json()
    assert get_user['email'] == 'test@mail.com'


@pytest.mark.django_db
def test_contact_user(client, user_factory):
    user = user_factory(_quantity=1)[0]
    contact_data = baker.prepare(Contact).__dict__
    assert contact_data.pop('_state')

    client.force_authenticate(user=user)
    url = f"{URL}contact/"
    post_response = client.post(url, data=contact_data).json()
    assert post_response['Status'] == '201'

    contact = Contact.objects.filter(user_id=user.pk).first()
    assert contact.city == contact_data['city']


@pytest.mark.django_db
def test_confirm_account(client, user_factory, confirm_email_token_factory):
    user = user_factory(_quantity=1)[0]
    conf = confirm_email_token_factory(_quantity=1)[0]
    conf.user = user
    conf.save()
    assert conf.user == user

    user_data = {
        'email': user.email,
        'token': conf.key
    }
    url = f'{URL}confirm/'

    post_response = client.post(url, data=user_data).json()
    assert post_response['Status'] == True
