from confluent_kafka import Producer
import snscrape.modules.twitter as sntwitter
from ..kafka_config import read_ccloud_config



# stores the details of the request w/ the corresponding parameters
mappedDetails = map()


def get_params(request_number: int):
    return mappedDetails[request_number]

def produce_Tweet_details(request_number: int,params: list[int]):
    """
    creates a request that is stored into the broker w/ the following details
    - client_request
    - parameters in order to execute the georender: X and Y coordinates    
    """
    
    producer = Producer(read_ccloud_config("../client.properties"))
    producer.produce("twitter-production" , key=request_number, value=params)

