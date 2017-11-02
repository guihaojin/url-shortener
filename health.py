# health check handler

def check(event, context):
    return {
        "statusCode": 200,
        "body": "OK"
    }
