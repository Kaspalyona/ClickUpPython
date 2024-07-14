import json
import os
import random
import string

import pytest
from dotenv import load_dotenv
from pytest_steps import test_steps

from helpers.session import Session
from methods.goals_steps import create_goal, delete_goal
load_dotenv()
base_url = os.getenv('BASE_URL')
goals_url = f'/team/{os.getenv("TEAM_ID")}/goal'
goal_url = '/goal/'

session = Session(base_url=os.getenv('BASE_URL'))

header_app_json = {
    'Content-Type': 'application/json',
}

@pytest.fixture
def create_goals_data():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    with open('TestData/create_goal.json', 'r') as f:
        body = json.load(f)
        body['name'] = random_string
    return body

@pytest.fixture
def get_goals_data():
    get_response = session.request('get', goals_url)
    body = json.loads(get_response.text)
    return body

@pytest.fixture
def get_goal_id():
    get_response = session.request('get', goals_url)
    body = json.loads(get_response.text)
    assert 'goals' in body and len(body['goals']) > 0, "No goals found in the response"
    return body['goals'][0]['id']
@pytest.fixture
def create_goals_invalid_data():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    with open('TestData/create_goal_invalid.json', 'r') as f:
        body = json.load(f)
    return body

@pytest.fixture
def deleted_goals_data(get_goal_id):
    id = get_goal_id
    delete_goal(session, goal_url + id)
    return id