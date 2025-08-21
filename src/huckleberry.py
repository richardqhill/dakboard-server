import os
import re

from datetime import datetime, timedelta
import pytz
from utils import request_with_retry

def get_time_since_last_bottle():
    # https://documenter.getpostman.com/view/8098574/SVSGNAGs
    
    # Make the API request with robust error handling
    response = request_with_retry(
        'https://dakboard.com/api/2/screens/scr_05c6be82a04e/blocks/blk_674797965a7ea652830ea032',
        params={'api_key': os.environ.get('DAKBOARD_API_KEY')}
    )
    
    # If request failed, return error response
    if response is None:
        return {
            "pretty": "🔴 API Error",
            "hours": 0,
            "minutes": 0,
            "error": "Failed to fetch data from Dakboard"
        }
    
    # Parse JSON response
    data = response.json()

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
        0: "🔴",
        1: "🔴",
        2: "🔴",
        3: "🤷‍♂️",
        4: "👍" 
    }
    emoji = hours2Emoji[hours] if hours in hours2Emoji else "🙌"
    
    return_string = f"{emoji} ~{hours}h {minutes}m"
    result = {
        "pretty": return_string,
        "hours": hours,
        "minutes": minutes,
    }
    
    return result

if __name__ == "__main__":
    get_time_since_last_bottle()
