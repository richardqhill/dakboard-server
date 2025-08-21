import os
import requests
import re

from datetime import datetime, timedelta
import pytz

# In-memory cache to avoid repeated Dakboard API calls within the same minute
_dakboard_cached_response: dict = {}
_dakboard_cached_minute_key: str = ""

def get_time_since_last_bottle():
    # https://documenter.getpostman.com/view/8098574/SVSGNAGs
    
    # Generate a minute-level cache key (e.g., "2024-01-15 14:30")
    now = datetime.now()
    current_minute_key = now.strftime("%Y-%m-%d %H:%M")
    
    global _dakboard_cached_response, _dakboard_cached_minute_key
    
    # Return cached response if we already have data for this minute
    if _dakboard_cached_minute_key == current_minute_key and _dakboard_cached_response:
        return _dakboard_cached_response
    
    # Make the API request
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
    
    # Store the result in Dakboard cache for this minute
    _dakboard_cached_response = result
    _dakboard_cached_minute_key = current_minute_key
    
    return result

if __name__ == "__main__":
    get_time_since_last_bottle()
