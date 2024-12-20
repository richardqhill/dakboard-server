import requests
import json
import re
from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)

params = {
    'api_key': os.environ.get('DAKBOARD_API_KEY'),
}

@app.route('/bottle')
def get_time_since_last_bottle():
    get_text_response = requests.get(
        'https://dakboard.com/api/2/screens/scr_05c6be82a04e/blocks/blk_674797965a7ea652830ea032',
        params=params,
    )

    content = json.loads(get_text_response.content)

    block_text = content["text"] if "text" in content else content["text' = "]


    times = list(filter(lambda x: x != '', block_text.split(' ')))
    bottle_time = re.sub(r'/[\d]+:/[\d+]\S', '', times[0]).replace('\r','').replace('\n',' ').replace(' ','').replace(' ','')

    # handle chinese lol

    is_from_yesterday = "PM" in bottle_time and datetime.now().hour < 12
    days_to_subtract = 1 if is_from_yesterday else 0

    bottle_datetime = datetime.strptime(bottle_time, "%I:%M%p") - timedelta(days=days_to_subtract)
    now  = datetime.now()
    duration = now - bottle_datetime
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60

    return_string = f"(~{hours}h {minutes}min)"
    return {
        "pretty": return_string,
        "hours": hours,
        "minutes": minutes,
    }

@app.route('/tesla')
def get_tesla_stats():
    return {
        "battery": 999,
        "miles": 999,
    }

if __name__ == '__main__':
    app.run(port=8080, debug=True)
    # get_time_since_last_bottle()