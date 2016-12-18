import json
import os
import time

from django.contrib.auth.models import User

import requests
from requests.auth import HTTPBasicAuth


def wait_for_firefox(selenium):
    pause = int(os.environ.get('FIREFOX_PAUSE', 5))
    if hasattr(selenium, 'firefox_profile'):
        time.sleep(pause)


def create_fred():
    return User.objects.create_user(
        username="fflint", email="fred@bedrock.com", password="wilma",
        first_name="Fred", last_name="Flintstone"
    )


def login(selenium, user, password):
    # He enters his username.
    user_field = selenium.find_element_by_name('username')
    user_field.send_keys(user)
    # And password (should pick something more secure).
    password_field = selenium.find_element_by_name('password')
    password_field.send_keys(password)
    # And logs in.
    button = selenium.find_element_by_name('login')
    button.click()
    wait_for_firefox(selenium)


def test_debt_api_creation(live_server):
    fred = create_fred()
    payload = {'title': 'A new debt entry'}
    headers = {'content-type': 'application/json'}

    response = requests.post(
        live_server.url + '/nimble/api/debts/', data=json.dumps(payload),
        headers=headers, auth=HTTPBasicAuth('fflint', 'wilma')
    ).json()
    print(response)
    assert response['title'] == payload['title']
    assert response['author']['username'] == fred.username


def test_feature_api_creation(live_server):
    fred = create_fred()
    payload = {'title': 'A new feature entry'}
    headers = {'content-type': 'application/json'}

    response = requests.post(
        live_server.url + '/nimble/api/features/', data=json.dumps(payload),
        headers=headers, auth=HTTPBasicAuth('fflint', 'wilma')
    ).json()
    print(response)
    assert response['title'] == payload['title']
    assert response['author']['username'] == fred.username
