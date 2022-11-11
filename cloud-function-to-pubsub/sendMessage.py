import requests
import json

def send_message_to_google_cloud():
    url = "MY_CLOUD_FUNCTION_TRIGGER_URL"
    data = {
        'sensorName': 'garden-sensor-001',
        'temperature': 84.0, 
        'humidity': 50
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(f'r = {r}')

if __name__ == '__main__':
    send_message_to_google_cloud()
