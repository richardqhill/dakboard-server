import os
import math
import json
import time
import hashlib
import hmac
import base64
import uuid
import requests

def generate_switchbot_header():
    # https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file#authentication
    
    apiHeader = {}
    token = os.environ.get('SWITCHBOT_TOKEN')
    secret = os.environ.get('SWITCHBOT_SECRET')
    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

    apiHeader['Authorization']=token
    apiHeader['Content-Type']='application/json'
    apiHeader['charset']='utf8'
    apiHeader['t']=str(t)
    apiHeader['sign']=str(sign, 'utf-8')
    apiHeader['nonce']=str(nonce)

    return apiHeader


def get_switchbot_devices():
    switchbot_response = requests.get(
        'https://api.switch-bot.com/v1.1/devices',
        headers = generate_switchbot_header()
    )
    content = json.loads(switchbot_response.content)

    print(content)


def get_switchbot_stats():
    device_id = os.environ.get('SWITCHBOT_METER_ID')

    switchbot_response = requests.get(
        f'https://api.switch-bot.com/v1.1/devices/{device_id}/status',
        headers = generate_switchbot_header()
    )
    content = json.loads(switchbot_response.content)

    temp_in_c = content["body"]["temperature"]
    temp_in_f = math.floor((int(temp_in_c) * 9 / 5) + 32)
    humidity = content["body"]["humidity"]
    
    return {
        "temp": temp_in_f,
        "humidity": humidity,
    }

if __name__ == "__main__":
    get_switchbot_devices()