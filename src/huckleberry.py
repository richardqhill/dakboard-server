import os
import requests
import re

from datetime import datetime, timedelta
import pytz

def get_time_since_last_bottle():
    # https://documenter.getpostman.com/view/8098574/SVSGNAGs
    
    get_text_response = requests.get(
        'https://dakboard.com/api/2/screens/scr_05c6be82a04e/blocks/blk_674797965a7ea652830ea032',
        params = {
            'api_key': os.environ.get('DAKBOARD_API_KEY'),
        }
    )
    data = get_text_response.json()

    block_text = data["text"] if "text" in data else data["text' = "]
    
    # remove \u202f NARROW NO-BREAK SPACE
    clean_block_text = re.sub(r"\u202f", "", block_text)

    pattern = r"(\d{1,2}:\d{2}[APM]{2})"
    timestamps = re.findall(pattern, clean_block_text)

    bottle_time = timestamps[0]

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
        3: "👍" 
    }
    emoji = hours2Emoji[hours] if hours in hours2Emoji else "🙌"
    
    return_string = f"{emoji} ~{hours}h {minutes}m"
    return {
        "pretty": return_string,
        "hours": hours,
        "minutes": minutes,
    }

if __name__ == "__main__":
    get_time_since_last_bottle()
