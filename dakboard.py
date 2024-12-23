import requests
import json

from datetime import datetime, timedelta
import os

from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
   os.environ.get('WEB_SERVER_USERNAME'): os.environ.get('WEB_SERVER_PASSWORD')
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
def hello_world():
    return "hello world"

@app.route('/bottle', methods=['GET'])
@auth.login_required
def get_time_since_last_bottle():
    get_text_response = requests.get(
        'https://dakboard.com/api/2/screens/scr_05c6be82a04e/blocks/blk_674797965a7ea652830ea032',
        params = {
            'api_key': os.environ.get('DAKBOARD_API_KEY'),
        }
    )

    content = json.loads(get_text_response.content)

    block_text = content["text"] if "text" in content else content["text' = "]

    times = list(filter(lambda x: x != '', block_text.split(' ')))
    bottle_time = times[0].replace('上午','AM').replace('下午','PM').replace('\r','').replace('\n',' ').replace(' ','').replace(' ','')

    is_from_yesterday = "PM" in bottle_time and datetime.now().hour < 12
    days_to_subtract = 1 if is_from_yesterday else 0

    bottle_datetime = datetime.strptime(bottle_time, "%I:%M%p") - timedelta(days=days_to_subtract)
    now  = datetime.now()
    duration = now - bottle_datetime
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60

    if hours <= 1:
        emoji = "🔴" 
    elif hours <= 2:
        emoji = "🤷‍♂️" 
    else:
        emoji = "👍" 

    return_string = f"{emoji} ~{hours}h {minutes}m"
    return {
        "pretty": return_string,
        "hours": hours,
        "minutes": minutes,
    }

@app.route('/tesla', methods=['GET'])
@auth.login_required
def get_tesla_stats():
    try:
        response = requests.get(
            'http://localhost:8080/api/v1/cars/1/status'
        )

        content = json.loads(response.content)

        battery_level = content['data']['status']['battery_details']['usable_battery_level']
        est_range = content['data']['status']['battery_details']['rated_battery_range']
        # plugged_in = content['data']['status']['charging_details']['plugged_in']
        # last_update = content['data']['status']['state_since']

        return {
            "battery": int(battery_level),
            "miles": int(est_range),
        }
    except:
        return {
            "battery": 0,
            "miles": 0,
        }

if __name__ == '__main__':
    app.run(port=8000, debug=True)