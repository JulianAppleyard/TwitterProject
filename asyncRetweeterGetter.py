#julian appleyard
#version November 17th 2018


import tweepy #http://docs.tweepy.org/en/v3.6.0/


import networkx as nx


import json
import time
import asyncio


access_token= "1043132884759072769-aqQYY7XQ2Rlj5CdXdLRgv0I3us3Dxs"
access_token_secret = "hIdttcfhoLqvoNVVvs7myVocBlVoKisqGgonqrk6WFXAh"
consumer_key= "YAUrjz6OEkKtVsnNuG0ZfdI7t"
consumer_secret= "vs6i2CdSphMn9MXoNg2azdSMqL0fzjQxIpLYXud3CajqFj8xZw"


#authetication requests
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


#create api variable
api = tweepy.API(auth)





# tweet_id should always be the tweet object of the original poster




    # Takes a string corresponding to how the API call is called in rate limit response json
        # api_string should be formated "/parent_string/restofstring" if it isnt, fix it
        # e.g here https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-show-id
            ## that call should be written /statuses/show/:id
def countdown(api_string):
    if not api_string.startswith('/'):
        api_string= '/' + 'api_string}'

    rate_status = api.rate_limit_status() #GET /application/rate_limit_status
    empty, parent_string, child = api_string.split("/", 2)
    reset_time = rate_status['resources'][parent_string][api_string]['reset']
    #Rate status returns the time the window resets (in UTC seconds since the epoch) before another request of this type can be made
    #take the time of reset - integer representation of current time to get seconds remaining
    time_left = reset_time - int(time.time())
    print('\n')
    while time_left:
        mins, secs = divmod(time_left, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Waiting {timeformat} before making another {api_string} call", end='\r')
        time.sleep(1)
        time_left -= 1





    # Handles the Twitter API rate limitation for iterator/cursor objects
def limit_handled(cursor, api_string):
    while True:
        try:
            yield cursor.next()
        except StopIteration:
            return
        except tweepy.RateLimitError:
            print(f"Rate Limit Exceeded for {api_string}")
            countdown(api_string)


'''
    Takes a tweet id and returns up to 100 of the most recent retweet objects in a list of status objects

'''
def get_more_retweets(tweet_id):
    while True:
        api_string = '/statuses/retweets:id'
        try:
            retweets = api.retweets(tweet_id, 100) #GET /statuses/retweets/:id
            print(f"Sent GET {api_string} and got {len(retweets)} new retweets")
                # Returns up to 100 of the first retweets objects of a given tweet as a list
                # Rate limited at 75/300 per 15 min window
            return retweets
        except tweepy.RateLimitError as e:
            print("Rate limted exceeded while gathering retweets for ", tweet_id)
            print(e)
            countdown(api_string)
        except Exception as e:
            print("Error ", e)





'''
# Takes a list of retweet objects and the original tweet object
# Finds follower relationships between them
# returns digraph coverted to dict of dicts
'''
def build_network(list_of_retweets, original_tweet_object):
    digraph = nx.DiGraph() #directed graph object
    # https://networkx.github.io/documentation/stable/reference/classes/digraph.html

    list_of_user_ids = [original_tweet_object.user.id] # The first in the list is always the original poster

    for tweet in list_of_retweets: #add the retweeters to the list
        list_of_user_ids.append(tweet.user.id)


    for source_id in list_of_user_ids:
        '''
        if
        #if account has a lot of followers use GET /friendships/lookup 15 requests for 15 min
        #but this is so slow...
        #could use this heuristically to 'guess' where connections might be to save time but
        #is this wortht the time?
            api_string = '/friendships/lookup'
            for target_id in list_of_users:
                try:
                    friendship_obj = api.show_friendship(source_id, target_id)
                    #Returns detailed information about the relationship between two users as a friendship object
                    #GET /friendships/lookup 15 requests for 15 min

                except tweepy.RateLimitError:
                    print(e)
                    countdown(api_string)

        else:
        '''
        print(f"Checking followers of {source_id} for retweets)
        api_string = '/followers/ids'
        for follower_id in limit_handled(tweepy.Cursor(api.followers_ids, id = source_id).items(), api_string):

            # Rate limited to 15 Requests in 15 min

            if (follower_id in list_of_user_ids): # https://networkx.github.io/documentation/stable/reference/classes/generated/networkx.DiGraph.has_node.html#networkx.DiGraph.has_node
                # If the account following the source_id is someone who retweeted the tweet
                # We can assume that they retweeting it from source_id
                # In the case where they are following multiple members of the list of ids, the one added earlier to the list will take precedent
                digraph.add_edge(source_id, follower_id)
    #convert digraph to dict of dict before returning
    print(f"Built retweet digraph for tweet id: {original_tweet_object.user.id} with {len(digraph.node)} nodes") #debug
    dict_dict = nx.to_dict_of_dicts(digraph)
    return dict_dict






def main():
    # https://twitter.com/brendonfacts/status/1064292313797668869
    tid = 1064292313797668869

    list_of_ids = [tid] #must not exceed 100 tweets
    print(f"Running main on {len(list_of_ids)} original statuses") #debug
    dict_of_tweets = {}
    for id in list_of_ids:
        dict_of_tweets[id] = [] #this is a list of retweet objects
        #later implementation can make this a previously obtained list of retweeters
    while True:
        # First get all tweet objects
        api_string = '/statuses/lookup'
        list_of_objects = []
        try:

            list_of_objects = api.statuses_lookup(id_ = list_of_ids) #GET /statuses/lookup
            print(f"Ran {api_string} successfully") #debug
            #   Returns fully-hydrated Tweet object for up to 100 Tweets per request
                ##   https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-lookup
                ##  900(user)/300(app) requests in a 15-min window
            break
        except tweepy.RateLimitError as e:
            print("Rate limted exceeded while gathering list of tweet objects ")
            print(e)
            countdown(api_string)

    for tweet in list_of_objects:
        new_count = tweet.retweet_count
        #if new_count >= (old_count + 50): could test so as to not make too many requests
        more_retweets = get_more_retweets(tweet.id)
        new_rts = []
        existing_rts = dict_of_tweets[tweet.id]
        # Make sure we are not adding duplicate rewtweet objects
        for retweet in more_retweets:
            if len(existing_rts) == 0:
                new_rts.append(retweet)
            else:
                for old_rt in existing_rts:
                    if not retweet.id == old_rt.id:
                        new_rts.append(retweet)
        dict_of_tweets[tweet.id] = existing_rts + new_rts
        print(f"Building graph from {len(dict_of_tweets[tweet.id])} retweets") #debug
        graph_as_dicts = build_network(dict_of_tweets[tweet.id], tweet)
        digraph = nx.from_dict_of_dicts(graph_as_dicts)
        print(f"Graph has {len(digraph.node)} nodes") #debug
        file_name = f'{tweet.id}.gml'
        path = '/gmlGraphs/' + file_name
        nx.write_gml(digraph, path)
        print("File saved as " + file_name) #debug





main()




#print(len(get_more_retweeters(tweet_id)))
