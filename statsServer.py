import config
import requests

def sendStatus(room, command, value):
    try:
        url = config.RCC_URL + "/room/status"
        querystring = {"id": "1"}
        payload = "r=" + room + "&n=" + command + "&v=" + value
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        auth_values = (config.RCC_USER, config.RCC_PASS)
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, auth=auth_values,
                                    verify=False)
        return response.text
    except:
        pass


def sendHeartbeat(room):
    try:
        url = config.RCC_URL + "/room/heartbeat"
        payload = "r=" + room
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        auth_values = (config.RCC_USER, config.RCC_PASS)
        response = requests.request("POST", url, data=payload, headers=headers, auth=auth_values, verify=False)
        return response.text
    except:
        pass

