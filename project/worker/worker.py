import redis
import json
import os
from time import sleep
from random import randint

if __name__ == '__main__':
    redis_host = os.getenv('REDIS_HOST', 'queue')
    reference = redis.Redis(host=redis_host, port=6379, db=0)
    print('Waiting messages...')
    while True:
        message = json.loads(reference.blpop('sender')[1])
        print('Sending message: ', message['subject'])
        sleep(randint(5, 10))
        print('Message', message['subject'], 'was sent sent')