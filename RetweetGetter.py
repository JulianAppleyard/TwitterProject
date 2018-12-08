#julian appleyard
#version November 27th 2018


import tweepy #http://docs.tweepy.org/en/v3.6.0/


import networkx as nx


import pickle
import json
import time
#import asyncio #for making this asyncronous later
import os.path # For saving filees to specific paths
import matplotlib.pyplot as plt # For drawing digraphs
from datetime import datetime, timedelta

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
    time_left = reset_time - int(time.time()) +1
    print('\n \r')
    while time_left:
        mins, secs = divmod(time_left, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(f" Waiting {timeformat} before making another {api_string} call", end='\r')
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
    Takes a tweet id and returns up to 100 of the most recent retweet objects as a list of status objects

'''
def get_more_retweets(tweet_id):
    while True:
        api_string = '/statuses/retweets:id'
        try:
            retweets = api.retweets(tweet_id, 100) #GET /statuses/retweets/:id
            print(f"Sent GET {api_string} for {tweet_id} and got {len(retweets)} retweets") #debug
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
# Takes the full list of retweet objects and the original tweet object
# Finds follower relationships between them
# returns digraph of user ids coverted to dict of dicts
'''
def build_network(list_of_retweets, original_tweet_object, existing_graph = {}):
    digraph = nx.DiGraph() #directed graph object

    if existing_graph != {}:
        digraph = nx.from_dict_of_dicts(existing_graph, create_using = nx.DiGraph())
        new_ids = []
        for tweet in list_of_retweets:
            if not digraph.has_node(tweet.user.id): #if the retweeter is already in the graph we dont need to recheck where they retweeted from
                new_ids.append(tweet.user.id)
        for id in new_ids:
            print(f"Who does {id} follow who already retweeted this tweet?") #debug
            api_string = '/friends/ids'
            for friend_id in limit_handled(tweepy.Cursor(api.friends_ids, id = id).items(), api_string):
                if digraph.has_node(friend_id):
                    #If they are following someone who (re)tweeted the tweet, they probably tweeted it from them
                    digraph.add_edge(friend_id, id)


    # https://networkx.github.io/documentation/stable/reference/classes/digraph.html

    # If we are making a new graph
    if existing_graph == {}:
        list_of_user_ids = [original_tweet_object.user.id] # The first in the list is always the original poster

        for tweet in list_of_retweets:
            list_of_user_ids.append(tweet.user.id)
        digraph.add_nodes_from(list_of_user_ids)

        for counter, source_id in enumerate(digraph.nodes()):
            print(f"{counter} Checking followers of {source_id} for retweets")
            api_string = '/followers/ids'
            for follower_id in limit_handled(tweepy.Cursor(api.followers_ids, id = source_id).items(), api_string):
                # Rate limited to 15 Requests in 15 min

                if (digraph.has_node(follower_id)): # https://networkx.github.io/documentation/stable/reference/classes/generated/networkx.DiGraph.has_node.html#networkx.DiGraph.has_node
                    # If the account following the source_id is someone who retweeted the tweet
                    # We can assume that they retweeting it from source_id
                    # In the case where they are following multiple members of the list of ids, the one added earlier to the list will take precedent
                    #print(f'Making edge between {source_id} and {follower_id}')
                    digraph.add_edge(source_id, follower_id)

    #Code to fix symmetric edges
    #We don't want symmetrical edges because we want a retweet network that shows how the tweet travelled
    #it doesn't travel backwards

    print(f'Checking {original_tweet_object.id} graph for symmetrical edges')
    while True:
        node_removed = False
        for edge1 in digraph.edges:
            #edges are represented as tuples like this: (u,v)
            #if there are directed edges (u,v) and (v, u) then we need to remove one
            #edge2 = (edge1[1], edge1[0])
            if digraph.has_edge(edge1[1], edge1[0]):
                print(f'Nodes {edge1[0]} and {edge1[1]} have symmetric edges between them.')
                u = {}
                v = {}
                #find these nodes in the list of retweet objects but also include the original tweet object
                list_of_retweets.append(original_tweet_object)
                for rt in list_of_retweets:
                    if rt.user.id == edge1[0]:
                        u = rt
                    elif rt.user.id == edge1[1]:
                        v = rt
                #remove the edge which goes from the newer retweet.user to the older one
                if u.created_at > v.created_at: #created_at returns datetime objects
                    digraph.remove_edge(u.user.id, v.user.id)
                    print(f'Removed edge between {v.user.id} and {u.user.id}') #debug
                    node_removed = True
                    break
                else:
                    digraph.remove_edge(v.user.id, u.user.id)
                    print(f'Removed edge between {u.user.id} and {v.user.id}')#debug
                    node_removed = True
                    break
                # if the loop removes an edge then it will need to restart because the digraph has changed
        if node_removed == False: break #if the for loop completes without removing any nodes, then break the while loop
    '''

    Do I want to fix redundant paths?
    '''

    dict_dict = nx.to_dict_of_dicts(digraph)
    return dict_dict






def main():

    # https://twitter.com/J_Appleyard/status/1062714222663081984
    tid = 1062714222663081984

    # https://twitter.com/brendonfacts/status/1064292313797668869
    # https://twitter.com/lxrdxyz/status/1064397964238573568
    # https://twitter.com/TFerrara2/status/1064025163342200832
    # https://twitter.com/maddymcconnon88/status/1063959627761680386
    # https://twitter.com/pcyIine/status/1067471643113594887
    # https://twitter.com/IAmMekoB/status/1067605231817670657
    list_of_ids = [tid, 1067605231817670657, 1064397964238573568, 1064292313797668869, 1064025163342200832, 1063959627761680386] #must not exceed 100 tweets

    '''
        NEED TO READ FILE(S) HERE
    '''
    storage = {}
    with open('storage.pkl', 'rb') as f:
        storage = pickle.load(f)

    # Read file containing a dictionary
    ## Where dict[tweet_id]['retweets'] contains a list of retweet objects
    ## and dict[tweet_id]['digraph'] contains a digraph representated as a dictionary of dictionaries




    print(f"Running main on {len(list_of_ids)} original statuses") #debug




    '''
    CHANGE THIS TO NOT USE TRY CATCH AND TO HANDLE WHEN LIST OF RETWEETS IS EMPTY
    '''
    for id in list_of_ids:

        try:
            dict_of_tweets = {}
            dict_of_tweets[id] = storage[id]['retweets']
            print(f"{id} is a previously analyzed tweet") #debug
        except KeyError as e:
            storage[id] = {}
            storage[id]['retweets'] = []
            storage[id]['digraph'] = {}
            print(f"{id} is a new tweet") #debug




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
        existing_rts = storage[tweet.id]['retweets']
        existing_graph = storage[tweet.id]['digraph']
         #debug
        # Make sure we are not adding duplicate rewtweet objects
        if len(existing_rts) == 0:
            new_rts = more_retweets
        else:
            existing_rt_ids = []
            for retweet in existing_rts:
                existing_rt_ids.append(retweet.id)
            for retweet in more_retweets:
                if not retweet.id in existing_rt_ids:
                    new_rts.append(retweet)
        if len(new_rts) == 0:
            print(f"Tweet {tweet.id} has no new retweets")
            continue


        total_rts= existing_rts + new_rts
        storage[tweet.id]['retweets']  = total_rts

        print(f"Building graph for {tweet.id} from {len(new_rts)} new retweets and {len(existing_rts)} existing retweets") #debug
        graph_as_dicts = build_network(total_rts, tweet, existing_graph)






        digraph = nx.from_dict_of_dicts(graph_as_dicts, create_using = nx.DiGraph())
        print(f"Graph has {len(digraph.node)} nodes") #debug




        # To save digraph as .gml file for Gephi
        file_name = f'{tweet.id}.gml'
        current_path = os.path.abspath("")
        path = os.path.join(current_path, 'gmlGraphs')
        path = os.path.join(path, file_name)
        nx.write_gml(digraph, path)
        print("File saved as " + file_name) #debug

        # To draw digraph with matplotlib and save the plot
        plt.clf()
        plt_name = f'{tweet.id}'
        nx.draw_networkx(digraph, arrows = True, with_labels = False)
        limits = plt.axis('off')
        plt.draw()
        plt.savefig(plt_name)
        print(f'Plot saved as {plt_name}.png')


        storage[tweet.id]['digraph'] = graph_as_dicts
        with open('storage.pkl', 'wb') as f:
            pickle.dump(storage, f)
        # To save digraph and retweet list in pickle file



main()




#print(len(get_more_retweeters(tweet_id)))
