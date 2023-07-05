
from datetime import datetime, timedelta
from decouple import config
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

import mongoengine

## TODO: we can also connect the user backend in order to maintain the database

# mongoengine.connect(
#     #Connect to MongoDB
#     db=config('MONGO_DB'), 
#     host = config('MONGO_HOST'),
#     port = int(config('MONGO_PORT',27017)),
#     username=config('MONGO_USER'), 
#     password=config('MONGO_PASS'), 
# )


class User(BaseModel):
    """
    User Model
    """
    username: str
    request_token: str
    access_token: str
    history_tweets: str



    