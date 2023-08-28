# from twitter_bot import TwitterAccess
# from kafka import Consumer, Producer
# from dotenv import load_dotenv
# import os
# import uvicorn


# load_dotenv()

# global twitter
# global consumer
# global producer

# async def setup_twitter():
#     twitter = TwitterAccess(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'), os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_KEY_SECRET'))
#     consumer = Consumer(workdetails)
#     producer = Producer(workdetails)

# async def consume_tweets():
#     try:
#         consumer.subscribe(['web3_tweets'])
#         while True:
#             msg = consumer.poll(1.0)
                    
#             if msg is None:
#                 continue
#             if msg.error():
#                 print("Consumer error: {}".format(msg))
                
                
#             ## now calling the function to write the tweet for the corresponding message
            
#             tweet_data = msg.value().decode('utf-8')
#             tweet_data = tweet_data.split(",")
#             print('message consumed' + tweet_data)
#             tweet(tweet_data[0],tweet_data[1])
#     except KafkaError as e:
#         print(e)

# @app.post('/api/twitterbot/produce/')
# async def producetweets(text:str,username:str):
#     try:
#         producer.produce('web3_tweets', text + "," + username)
#         producer.flush()
#     except Exception as e:
#         print(e)
    
    
# @app.post('/api/twitterbot/tweet')
# async def tweet(text:str,username:str):
#     try:
#         twitter.write_tweet(text,username)    
#     except Exception as e:
#         print(e) 


# @app.get("/api/twitterbot/get_tweets")      
# async def get_user_tweets(username:str):
#     try:
#         user_tweets = twitter.get_user_tweets(username)
#         return user_tweets
#     except Exception as e:
#         print(e)

# if __name__ == "__main__":
#      uvicorn.run(app, host="127.0.0.1", port=8000)
