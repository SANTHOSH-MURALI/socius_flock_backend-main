import uuid
from flask import request
import time

def get_random_id():
    return uuid.uuid4().hex

def get_curent_session():
    return request.headers['Session-Id']

def millis():
    return int(round(time.time() * 1000))