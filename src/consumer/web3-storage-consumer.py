from confluent_kafka import Consumer
from ..kafka_config import read_ccloud_config

"""
this will be fetching the request from the broker (consisting of the user id in order to store the file directly)
"""
def consume_stream():

    props = read_ccloud_config("../client.properties")
    props["group.id"] = "python-group-1"
    props["auto.offset.reset"] = "earliest"

    consumer = Consumer(props)
    consumer.subscribe(["web3-storage-production"])
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                print("key = {key:12} value = {value:12}".format(key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
