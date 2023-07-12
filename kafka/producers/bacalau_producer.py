from confluent_kafka import KafkaException
from async_producer_template import AsyncProducer
from ..kafka_config import read_ccloud_config
from  fastapi import FastAPI
from ..model import Bacalhaujobparams

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global  producer
    conf = read_ccloud_config()
    producer = AsyncProducer(conf)


@app.on_event("shutdown")
def shutdown_event():
    producer.close()

@app.post("/bacalhau/")

def produce_bacalau_topic(params: Bacalhaujobparams):
    """
    generates the bacalau job message and then sends to tge kafka topic
     params: this corresponds to the 

    """
    try:
      return_job_id  =  producer.produce("bacalau-job", value=params)
    except KafkaException as e:
        print(e)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
    


    