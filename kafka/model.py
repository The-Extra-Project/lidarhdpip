from pydantic import BaseModel, StrictStr

class TwitterProducerMessage(BaseModel):
    name: StrictStr
    coordinateX: StrictStr
    coorindateY: StrictStr
    topic: StrictStr
    timestamp: StrictStr = ""

class tweetProducerResponse():
    coordX: int
    coordY: int
    tweet_id: int




class Web3StorageProducerMessage(BaseModel):
    cid: StrictStr

