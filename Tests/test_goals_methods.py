import json
import logging
import os
import random
import string

import pytest
from dotenv import load_dotenv
from pytest_steps import test_steps
from fixtures.goals_config import *
from helpers.session import Session
from methods.goals_steps import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
load_dotenv()

base_url = os.getenv('BASE_URL')
goals_url = f'/team/{os.getenv("TEAM_ID")}/goal'
goal_url = '/goal/'

session = Session(base_url=os.getenv('BASE_URL'))


header_app_json = {
    'Content-Type': 'application/json',
}


@test_steps('Get goals')
def test_goals_get(test_step):
    get_response = session.request('get', goals_url)
    assert get_response.status_code == 200

@test_steps('Create goal')
def test_goals_send_data(test_step, create_goals_data):
    send_response = session.request('post', goals_url, headers=header_app_json, data=json.dumps(create_goals_data))
    assert send_response.status_code == 200


#create tests to make positive and negative tests for endpoints use goal_id
@pytest.mark.parametrize('goal_id, expected_status_code', [
    (None, 200),
    ('', 404),
    ('invalidtype', 500),
])
@test_steps('Get goal', 'Update goal', 'Delete goal')
def test_goal_workflow(goal_id, expected_status_code, get_goal_id, create_goals_data,test_step):
    if test_step == 'Get goal':
        if goal_id is None:
            goal_id = get_goal_id
        get_response = get_goal(session, goal_url+goal_id)
        assert get_response.status_code == expected_status_code

    elif test_step == 'Update goal':
        if goal_id is None:
            goal_id = get_goal_id
        put_goal_response = update_goal(session, goal_url+goal_id, create_goals_data)
        assert put_goal_response.status_code == expected_status_code

    elif test_step == 'Delete goal':
        if goal_id is None:
            goal_id = get_goal_id
        delete_response = delete_goal(session, goal_url+goal_id)
        assert delete_response.status_code == expected_status_code

@test_steps('Update goal with invalid body, no name')
def test_goals_update_not_valid_id(test_step, get_goal_id, create_goals_invalid_data):
    update_url = goal_url + get_goal_id
    put_goal_response = session.request('put', update_url, headers=header_app_json, data=json.dumps(create_goals_invalid_data))
    assert put_goal_response.status_code == 400

@test_steps('Delete non-existent goal')
def test_goals_delete_data(test_step, get_goal_id, deleted_goals_data):
    id = deleted_goals_data
    deleted_response = session.request('delete', goal_url + id);
    assert deleted_response.status_code == 404

# @test_steps('Update goal')
# def test_goals_update_data(test_step, get_goal_id, create_goals_data):
#     id = get_goal_id
#     update_url = goal_url + id
#     print(f"Updating goal at URL: {update_url}")
#     put_goal_response = session.request('put', update_url, headers=header_app_json, data=json.dumps(create_goals_data))
#     assert put_goal_response.status_code == 200
#
#     updated_goal_id = put_goal_response.json()['goal']['id']
#     assert updated_goal_id is not None
#     assert updated_goal_id == id
#
# @test_steps('Delete goal')
# def test_goals_delete_data(test_step, get_goal_id):
#     id = get_goal_id
#     deleted_response = session.request('delete', goal_url + id);
#     assert deleted_response.status_code == 200
#     return id
#


# @pytest.mark.parametrize('goal_id, expected_status_code', [
#     (None, 200),
#     ('', 404),
#     ('invalidtype', 500),
# ])
# @test_steps('Get goal')
# def test_get_goal(test_step, goal_id, expected_status_code, get_goal_id):
#     if goal_id is None:
#         goal_id = get_goal_id
#     get_response = session.request('get', goal_url + goal_id)
#     print(f"Testing goal_id: {goal_id} with expected status code: {expected_status_code}")
#     assert get_response.status_code == expected_status_code