#import the necessary methods from tweepy library
import tweepy
import codecs
#Variables that contain the user credentials to access Twitter API
access_token= "1043132884759072769-aqQYY7XQ2Rlj5CdXdLRgv0I3us3Dxs"
access_token_secret = "hIdttcfhoLqvoNVVvs7myVocBlVoKisqGgonqrk6WFXAh"
consumer_key= "YAUrjz6OEkKtVsnNuG0ZfdI7t"
consumer_secret= "vs6i2CdSphMn9MXoNg2azdSMqL0fzjQxIpLYXud3CajqFj8xZw"

#Authentication requests
auth= tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Create api variable
api = tweepy.API(auth)

public_tweets = api.home_timeline()

f= codecs.open("timeline.txt", "w", "utf-8")

for tweet in public_tweets:
    for p in tweet.__dict__.items():
        f.write("%s:%s\n" % p)
        f.write("\n")

f.close()
