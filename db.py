import os
import logging
import boto3

COUNTER_ID = "__id"
BASE = 64

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def get_url(id):
    item = table.get_item(Key={"id": id})
    try:
        return item['Item']['url']
    except Exception as e:
        logging.exception('No url for id: %s, exception: %s', id, e)
        return None


def shorten_url_helper(url):
    counter = generate_new_counter()
    key = convert_to_id(counter)
    table.put_item(Item={'id': key, 'url': url})
    logging.info('Generated key: %s for url: %s', key, url)
    return key


def generate_new_counter():
    ret = table.update_item(Key={'id': COUNTER_ID},
                            UpdateExpression='add #counter :n',
                            ExpressionAttributeNames={'#counter': 'counter'},
                            ExpressionAttributeValues={':n': 1},
                            ReturnValues='UPDATED_NEW')
    return int(ret['Attributes']['counter'])


# convert integer into base 62 string, characters from {0..9}, {A..Z}, {a..z}
def convert_to_id(n):
    if n == 0:
        return '0'
    ret = ''
    while n > 0:
        remainder = n % BASE
        ret = _true_chr(remainder) + ret
        n /= BASE
    return ret[1:] if len(ret) > 2 and ret[0] == '0' else ret


def _true_chr(integer):
    if integer < 10:
        return chr(integer + 48)
    elif 10 <= integer <= 35:
        return chr(integer + 55)
    elif 36 <= integer < 62:
        return chr(integer + 61)
    else:
        raise ValueError("%d is not a valid integer in the range of base 62" % integer)
