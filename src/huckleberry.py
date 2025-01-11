import os
import json
import requests

from datetime import datetime, timedelta
import pytz

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
    bottle_time = times[0].translate(str.maketrans({'\r': None, '\n': None, ' ': None, ' ': None}))

    origin_tz = pytz.timezone('America/New_York')
    now  = datetime.now(origin_tz)

    bottle_datetime = datetime.strptime(f"{now.year} {now.month} {now.day} {bottle_time}", "%Y %m %d %I:%M%p")
    bottle_datetime = origin_tz.localize(bottle_datetime)

    is_from_yesterday = "PM" in bottle_time and now.hour < 12
    if is_from_yesterday:
        bottle_datetime = bottle_datetime - timedelta(days=1)

    duration = now - bottle_datetime
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60

    hours2Emoji = {
        1: "🔴",
        2: "🤷‍♂️",
        3: "👍" ,
        4: "🙌",
        5: "🙌"
    }
    emoji = hours2Emoji[hours] if hours in hours2Emoji else "🔴"
    
    return_string = f"{emoji} ~{hours}h {minutes}m"
    return {
        "pretty": return_string,
        "hours": hours,
        "minutes": minutes,
    }
