import logging
import json

from db import get_url


def redirect(event, context):
    short_url = event["pathParameters"]["shortUrl"]
    redirect_url = get_url(short_url)
    if redirect_url:
        logging.info('Redirecting to url: %s', redirect_url)
        return {"statusCode": 308, "headers": {"location": redirect_url}}
    else:
        logging.info('Redirect url not found.')
        return {"statusCode": 404, "body": json.dumps({"message": "Not found"})}
