from tweepy.streaming import StreamListener
from tweepy import API, Tweet, Stream, OAuthHandler
'''
script for interacting w/ the users tweets on the twitter. 

to instantiate w/ the user's credentials, go to developer.twitter.com & get the following parameters from developer.twitter.com
access_token_key
access_token_secret
consumer_key
consumer_secret

and then access from the command line:
'''

class TwitterAccess():
    _tweepy_auth: OAuthHandler
    tweepy_api: API

    def __init__(self,access_token_key, access_token_secret,consumer_key, consumer_secret):
        self._tweepy_auth = OAuthHandler(consumer_key, consumer_secret, access_token_key, access_token_secret)
        self._tweepy_auth.set_access_token(self.access_token, access_token_secret)
        self.tweepy_api = API(self._tweepy_auth)

    def get_tweets(self,user_name, _count):
        tweets = self.tweepy_api.user_timeline(screen_name=user_name, count=_count)
        return tweets

    def fetch_geo_coordinates_tagged(self, _user_name, selected_tweet ):
        """
        Defines the location of the given tweet selected by the user
        """
        twitter_timeline = self.get_tweets(user_name=_user_name)
        for tweet in twitter_timeline:
            if tweet.id == selected_tweet:
                return tweet.coordinates
        return None

    def fetch_geo_coordinates_from_tweets(tweet_text):
        pattern = r"[-+]?\d+\.\d+,[-+]?\d+\.\d+"
        match_pattern = re.search(pattern,tweet_text)

        if match_pattern: 
            return match_pattern.group(0)        
        else:
            return None        

    def write_tweets(self,tweet_text):
        self.tweepy_api.update_status(status=tweet_text)