from confluent_kafka import Producer
import snscrape.modules.twitter as sntwitter
from ..kafka_config import read_ccloud_config

# stores the details of the request w/ the corresponding parameters
mappedTweets = map()

def get_params(request_number: int):
    return mappedTweets[request_number]

def produce_Tweet_details(request_number: int,params: list[int]):
    """
    creates a request that is stored into the broker queue
    - client_request parameters
    - parameters in order to execute the georender: X and Y coordinates    
    """
    
    producer = Producer(read_ccloud_config("../client.properties"))
    producer.produce("tweet-producer" , key=request_number, value=params)

def write_params(request_number: int, params: list(str) ):
     mappedTweets[request_number] = params

def read_params(request_number: int):
    return mappedTweets[request_number]