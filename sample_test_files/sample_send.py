import pika
import json

connection = pika.BlockingConnection(
pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="neom_0")
json_str = {
    "operational_data": {
        "imageLocation": "file loc",
        "locationData": [
            {
                "latitude": 35.01720428466797,
                "longitude": 28.101587947028705
            },
            {
                "latitude": 35.002394,
                "longitude": 28.110035
            },
            {
                "latitude": 10,
                "longitude": 10
            },
            {
                "latitude": 35.01820428466797,
                "longitude": 28.102587947028705
            },
            {
                "latitude": 35.01820428466797,
                "longitude": 28.102587947028705
            },
            {
                "latitude": 35.142984191,
                "longitude": 28.126704906
            }
        ]
    },
    "source": "NEOM Line",
    "capture_timestamp": "2021-12-19T14:02:33",
    "checkGeofence": True,
    "usecase": "Litter tracking"
}
channel.basic_publish(exchange="", routing_key="neom_0",
                      body=json.dumps(json_str))
print(f"Sent {json_str}")
connection.close()
