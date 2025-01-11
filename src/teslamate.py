import requests
import json

def get_tesla_stats():
    try:
        response = requests.get(
            'http://localhost:8080/api/v1/cars/1/status'
        )

        content = json.loads(response.content)

        battery_level = content['data']['status']['battery_details']['usable_battery_level']
        est_range = content['data']['status']['battery_details']['rated_battery_range']
        plugged_in = content['data']['status']['charging_details']['plugged_in']
        # 2025-01-10T14:38:17-05:00
        # last_update = content['data']['status']['state_since']

        return {
            "battery": int(battery_level),
            "miles": int(est_range),
            "plugged_in": bool(plugged_in),
            # "last_update": str(last_update)
        }
    except:
        return {
            "battery": 0,
            "miles": 0,
            "plugged_in": False,
            "last_update": "-1"
        }