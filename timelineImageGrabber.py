#import the necessary methods from tweepy library
import tweepy
import codecs
import wget
import json
#Variables that contain the user credentials to access Twitter API
access_token= "1043132884759072769-aqQYY7XQ2Rlj5CdXdLRgv0I3us3Dxs"
access_token_secret = "hIdttcfhoLqvoNVVvs7myVocBlVoKisqGgonqrk6WFXAh"
consumer_key= "YAUrjz6OEkKtVsnNuG0ZfdI7t"
consumer_secret= "vs6i2CdSphMn9MXoNg2azdSMqL0fzjQxIpLYXud3CajqFj8xZw"


#configuring tweepy to return json format

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

#status() is the dtat model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
#User() is the data model for a user profile
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
#You will need to do it for all the models you need

#Authentication requests
auth= tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


#Create api variable
api = tweepy.API(auth)


#this api call can only return 3200 of a user's most recent Tweets, up to 200 per call
tweets = api.user_timeline(screen_name='BrainMemes', count = 40, include_rts= False)

#create a dicionary with keys as ids and values as filenames (with file extension)
this_user_dictionary = {}


media_files = set()

for status in tweets:
    #print(status.text)
    media = status.entities.get('media', [])
    if(len(media) > 0):
        media_files.add(media[0]['media_url'])
        tweet_id = status.id_str
        this_user_dictionary[tweet_id]=
        print("added a media element")

#this implementation assumes that either each tweet has only one media attachment, or we only care about the first one
#at this stage, we have the urls of all the multimedia content stored in the variable media_files

#use python library wget to download the files in media_files
#twitter accepts GIF, JPEG, and PNG files
for media_file in media_files:
    print("Downloading image")
    wget.download(media_file, 'C:/Users/Julian/Documents/GitHub/TwitterProject/Images')
#this will download all the images (or any other multimedia content) into the current folder
#look into implementing a solution which creates a new folder, filters by specific type etc
