import os
import json
import logging

from db import shorten_url_helper


def shorten_url(event, context):
    data = json.loads(event['body'])
    logging.info('Request data: %s', data)
    if 'url' not in data:
        return {"statusCode": 400, "body": json.dumps({"message": "error: url not exist."})}
    endpoint = shorten_url_helper(data['url'])
    item = {
        'url': os.environ['SHORT_URL_HOST'] + endpoint,
    }
    response = {
        "statusCode": 201,
        "body": json.dumps(item)
    }
    return response
