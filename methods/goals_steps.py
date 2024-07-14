import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def get_goal(session, goal_path):
    logger.info('Sending GET request to %s with goal_id: %s', goal_path)
    get_response = session.request('get', goal_path)
    logger.info('Received response: %s', get_response.text)
    response_json = json.loads(get_response.text)
    print(response_json)
    return get_response

def create_goal(session, goal_path, create_goal_data):
    headers = {
        'Content-Type': 'application/json',
    }
    logger.info('Sending POST request to %s with data: %s', goal_path)
    response = session.request('post', goal_path, headers=headers, data=json.dumps(create_goal_data))
    logger.info('Received response: %s', response.text)
    return response

def update_goal(session, goal_path, create_goals_data):
    headers = {
        'Content-Type': 'application/json',
    }
    logger.info('Sending PUT request to %s with data: %s', goal_path)
    response = session.request('put', goal_path, headers=headers, data=json.dumps(create_goals_data))
    return response

def delete_goal(session, goal_path):
    headers = {
        'Content-Type': 'application/json',
    }
    logger.info('Sending DELETE request to %s', goal_path)
    response = session.request('delete', goal_path, headers=headers)
    logger.info('Received response: %s', response.text)
    return response
