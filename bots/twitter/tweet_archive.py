from twarc2 import Twarc2, expansions
from twarc2.exntensions import ensure_flattened
import json
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from datetime import datetime, timezone, timedelta
client = Twarc2(bearer_token="")
app = FastAPI()
import re
@app.get('/get_geoordinates/') 
def get_geo_coordinate_tweet():
    """
    function that gets the given geocoordinates from user tweets
    username: is the username which has messaged geocordinates along with other parameters from the user

    it then calls the kafka message passing the said geocoordinates    
    """
    
    load_dotenv(dotenv_path='./../.env')
    
    ## gets the last tweeted parameters from the user.
    ## needs to configure based on the user timezone, currently setting based on european time
    start_time = datetime.now(timezone.utc) + timedelta(hours=-2)
    end_time = datetime.now(timezone.utc) + timedelta(minutes=-1)
    
    query = "geospatial reconstruction: X= Y=  lang:en   "
    print("fetching the tweets consisting of the geospatial parameters from {} till {}".format(start_time, end_time))
    search_results = client.search_recent(query=query, start_time=start_time, end_time=end_time, max_results=10)


    results = []
    if search_results:
        for tweet in search_results:
            text = ensure_flattened(tweet)
            results.append(parse_params(text))
    return results
def parse_params(text_info) -> list(str):
    """
        parses the generated list of tweets and returns the parameters (geoocordinates)
    """ 
        ## 
    pattern_geo = '^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'
        
    return re.findall(pattern_geo,text_info)
       
if __name__ == '__main__':
    uvicorn.app(app, host="0.0.0.0", port=8000)
    