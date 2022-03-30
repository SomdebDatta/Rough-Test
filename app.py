print("hello")

import os
import sys
import pika
import json
from reading_geofence.polygon_extraction import get_polygon
from utility.objects_in_geofence import check_if_within_geo
from utility.converter import not_in_geofence, output_format, points_from_jsonip
import yaml

from logs.logger import get_logger
LOGGER = get_logger('rabbitmq_callback')

with open("./config/config.yaml") as reader:
    qs = yaml.load(reader, Loader=yaml.FullLoader)

def callback(ch, method, properties, body):
    input_json = json.loads(body.decode("utf-8"))
    LOGGER.info("Input data received - {0}".format(input_json))

    poly_coord = get_polygon(input_json['source'])
    LOGGER.info("Polygon Coordinates received. - {0}".format(poly_coord))
    print(poly_coord)

    points = points_from_jsonip(input_json["operational_data"]["locationData"])
    
    out = check_if_within_geo(points, poly_coord)
    if out: 
        json_str = output_format(input_json, out)
        send_msg(host = qs["database"]["host"], queue= qs["output_queue"], msg = json.dumps(json_str), routing_key= qs["output_queue"])
    else:
        json_str = not_in_geofence(input_json) 
    ch.basic_ack(delivery_tag = method.delivery_tag)


def send_msg(host, queue, msg, routing_key):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="", routing_key=routing_key, body=msg)
    LOGGER.debug("Output message - {0}".format(msg))
    connection.close()

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=qs["database"]["host"]))
    channel = connection.channel()
    channel.queue_declare(queue=qs["input_queue"])
    channel.basic_consume(queue=qs["input_queue"], on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
