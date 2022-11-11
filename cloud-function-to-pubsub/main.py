# make sure you're in the right project...
#   first check what's the current project:     terminal > gcloud config get-value project
# if that's the wrong project...
#   list all projects:                          terminal > gcloud projects list
#   then move to the right project              termainal > gcloud config set project PROJECT_ID

# to deploy this cloud function...
#   terminal > gcloud functions deploy FUNCTION_NAME --runtime python39 --trigger-http --allow-unauthenticated

#  helpful link: https://cloud.google.com/functions/docs/samples/functions-pubsub-publish

import base64
import json
import os
from google.cloud import pubsub_v1                                      # pip install google-cloud-pubsub

publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('MY_PROJECT_ID')                                 # GOOGLE_CLOUD_PROJECT


def my_cloud_function(request):
    data = request.data

    if data is None:
        print('request.data is empty')
        return ('request.data is empty', 400)

    print(f'request data: {data}')
    
    data_json = json.loads(data)                                        # turn the string into a dictionary
    print(f'json = {data_json}')

    sensor_name = data_json['sensorName']
    temperature = data_json['temperature']
    humidity = data_json['humidity']
    
    print(f'sensor_name = {sensor_name}')
    print(f'temperature = {temperature}')
    print(f'humidity = {humidity}')

    ###############################
    # move the data to Pubsub!

    topic_path = 'MY_PUBSUB_TOPIC_FULL_NAME'                    # Pubsub topic path

    message_json = json.dumps({
        'data': {'message': 'sensor readings!'},
        'readings': {
            'sensorName': sensor_name,
            'temperature': temperature,
            'humidity': humidity
        }
    })
    message_bytes = message_json.encode('utf-8')

    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()                                         # verify that the publish succeeded
    except Exception as e:
        print(e)
        return (e, 500)

    return ('Message received and published to Pubsub', 200)
