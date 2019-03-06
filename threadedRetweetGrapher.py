#julian appleyard
#version Feb 18th 2019
import twitter
import tweepy #http://docs.tweepy.org/en/v3.6.0/
import networkx as nx

import pickle


import requests
import time
import threading
from queue import Queue
import os.path # For saving filees to specific paths
import matplotlib.pyplot as plt # For drawing digraphs
import datetime

access_token= "1043132884759072769-aqQYY7XQ2Rlj5CdXdLRgv0I3us3Dxs"
access_token_secret = "hIdttcfhoLqvoNVVvs7myVocBlVoKisqGgonqrk6WFXAh"
consumer_key= "YAUrjz6OEkKtVsnNuG0ZfdI7t"
consumer_secret= "vs6i2CdSphMn9MXoNg2azdSMqL0fzjQxIpLYXud3CajqFj8xZw"


"""
    TWEEPY SETUP
"""

#authetication requests
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#create api variable
api = tweepy.API(auth)


"""
    PYTHON-TWITTER SETUP
"""
api_secondary = twitter.Api(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token_key = access_token, access_token_secret = access_token_secret)







retweet_queue = Queue()
builder_queue = Queue()
storage_lock = threading.Lock()


storage_path = os.path.join(os.path.abspath(""), 'storage') #this is the path where the graphs and data will be stored

main_sleep_time = 30 # how long the main thread sleeps before checking for updates to retweet count



'''
# Takes a string corresponding to how the API call is called in rate limit response json
    # api_string should be formated "/parent_string/restofstring" if it isnt, fix it
    # e.g here https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-show-id
        ## that call should be written /statuses/show/:id
'''
def countdown(api_string):
    if not api_string.startswith('/'):
        api_string= '/' + 'api_string}'

    rate_status = api.rate_limit_status() #GET /application/rate_limit_status
    empty, parent_string, child = api_string.split("/", 2)
    reset_time = rate_status['resources'][parent_string][api_string]['reset']
    #Rate status returns the time the window resets (in UTC seconds since the epoch) before another request of this type can be made
    #take the time of reset - integer representation of current time to get seconds remaining
    time_left = reset_time - int(time.time()) +1
    print('\n')
    mins, secs = divmod(time_left, 60)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)

    print(f" Waiting {timeformat} before making another {api_string} call from now: " + datetime.datetime.now().strftime('%b %d, %Y at %H:%M:%S')) #debug
    while time_left:

        time.sleep(1)
        time_left -= 1

'''
# Handles the Twitter API rate limitation for iterator/cursor objects
'''

def limit_handled(cursor, api_string):
    time.sleep(1)
    while True:
        try:
            yield cursor.next()
        except StopIteration:
            return
        except tweepy.error.RateLimitError:

            print(f"Rate Limit Reached for {api_string}")
            countdown(api_string)



class FirstCursorRateError(Exception):
    pass

def limit_handled_friend(cursor, api_string):
    time.sleep(1)
    while True:
        try:
            yield cursor.next()
        except StopIteration:
            return
        except tweepy.error.RateLimitError:
            if cursor.current_page is not None:
                print(f"Rate Limit Reached for {api_string}")
                countdown(api_string)
            else:
                raise FirstCursorRateError('This is blocking on the first request for this tweet')
                return





'''
# Takes an updated tweet object and first checks to see if it has
#Then checks this set of retweets against the existing list of retweets in storage
#It then adds only the new retweets to the existing list in storage and saves it back to storage
# returns
'''
def get_more_retweets(tweet):

    while True:
        api_string = '/statuses/retweets:id'
        try:
            #checking if there are actually any new retweets, because queue may have duplicated requests without new retweets occurring
            storage = {}
            with storage_lock:
                tweet_path = os.path.join(storage_path, f'{tweet.id}.pkl')
                with open(tweet_path, 'rb') as f:
                    storage = pickle.load(f)

            new_count = tweet.retweet_count
            old_rt_list = storage['retweets']
            if len(storage['retweets']) > 0:
                old_count = old_rt_list[-1].retweeted_status.retweet_count
            else:
                old_count = 0

            if new_count == old_count:
                print(f"Tweet {tweet.id} has no new retweets")#debug
                return
            print("Making GET for more retweets")
            more_retweets = api.retweets(tweet.id, 100) #GET /statuses/retweets/:id
            print(f"Sent GET {api_string} for {tweet.id} and got {len(more_retweets)} retweets") #debug
                # Returns up to 100 of the first retweets objects of a given tweet as a list
                # Rate limited at 75/300 per 15 min window

            with storage_lock:
                with open(tweet_path, 'rb') as f:
                    storage = pickle.load(f)
                new_rts = []

                existing_rts = storage['retweets']
                print(f"    Storage contains {len(existing_rts)} existing retweets")#debug
                # Make sure we are not adding dupilcate retweeet objects
                if len(existing_rts) == 0:
                    new_rts = more_retweets
                else:
                    existing_rt_ids =[]
                    for retweet in existing_rts:
                        existing_rt_ids.append(retweet.id)
                    for retweet in more_retweets:
                        if not retweet.id in existing_rt_ids:
                            new_rts.append(retweet)

                if len(new_rts) == 0:
                    print(f"    Tweet {tweet.id} has no new retweets")#debug
                    return
                else:
                    print(f"    Tweet {tweet.id} has {len(new_rts)} new retweets")
                    total_rts = existing_rts + new_rts
                    storage['retweets'] = total_rts


                    with open(tweet_path, 'wb') as f:
                        pickle.dump(storage, f)

                    return

        except tweepy.RateLimitError as e:
            print(f"Rate limted exceeded while gathering retweets for {tweet.id}")
            print(e)
            countdown(api_string)



'''
# This function first pulls an existing digraph from storage
# It then checks this digraph for symmetric edges
# If there is a symmetric edge, it removes the edge corresponding to a newer retweet

So for some tweet, if B and C follow each other and both retweeted it:
* the retweet objects are compared for the datetime in which they were posted
* the if B's retweet object is older than C's, then the edge from C to B is removed
* otherwise the opposite edge is removed

# and saves it to storage
# It then draws the graph a
'''

def orient_graph(tweet):

    '''
    #Code to fix symmetric edges
    #We don't want symmetrical edges because we want a retweet network that shows how the tweet travelled
    and it doesn't travel backwards
    '''
    print(f'Checking {tweet.id} graph for symmetric edges')
    storage ={}

    tweet_path = os.path.join(storage_path, f'{tweet.id}.pkl')

    #Locking for critical section of code
    with storage_lock:
        with open(tweet_path, 'rb') as f:
            storage = pickle.load(f)

        list_of_retweets = storage['retweets']
        digraph = nx.from_dict_of_dicts(storage['digraph'], create_using = nx.DiGraph())
        while True:
            edge_removed = False
            for edge1 in digraph.edges:
                #edges are represented as tuples like this: (u,v)
                #if there are directed edges (u,v) and (v, u) then we need to remove one

                #delete all edges coming into the OP
                if edge1[1] == tweet.user.id:
                    digraph.remove_edge(edge1[0], edge1[1])
                    edge_removed = True
                    break


                if digraph.has_edge(edge1[1], edge1[0]):
                    print(f'Nodes {edge1[0]} and {edge1[1]} have symmetric edges between them.')
                    u = {}
                    v = {}
                    #find these nodes in the list of retweet objects but also include the original tweet object
                    for rt in list_of_retweets:
                        if rt.user.id == edge1[0] or tweet.user.id == edge1[0]:
                            u = rt
                        elif rt.user.id == edge1[1] or tweet.user.id == edge1[1]:
                            v = rt



                    #if a person was unfollowed during this time, remove the offending edge
                    if u == {}:
                        digraph.remove_edge(edge1[0], edge1[1])
                        edge_removed = True

                        break
                    if v =={}:
                        digraph.remove_edge(edge1[1], edge1[0])
                        edge_removed = True
                        break



                    if u.created_at > v.created_at: #created_at returns datetime objects
                        digraph.remove_edge(u.user.id, v.user.id)
                        #print(f'Removed edge between {v.user.id} and {u.user.id}') #debug
                        edge_removed = True
                        break
                    else:
                        digraph.remove_edge(v.user.id, u.user.id)
                        #print(f'Removed edge between {u.user.id} and {v.user.id}')#debug
                        edge_removed = True
                        break
                    # if the loop removes an edge then it will need to restart because the digraph has changed
            if edge_removed == False: break #if the for loop completes without removing any nodes, then break the while loop


        dict_dict = nx.to_dict_of_dicts(digraph)

        storage['oriented'] = dict_dict

        with open(tweet_path, 'wb') as f:
            pickle.dump(storage, f)


    '''
    To save graph in various formats
    '''
    # To save digraph as .gml file for Gephi
    file_name = f'oriented{tweet.id}.gml'
    current_path = os.path.abspath("")
    path = os.path.join(current_path, 'gmlGraphs')
    path = os.path.join(path, file_name)
    nx.write_gml(digraph, path)
    print("File saved as " + file_name) #debug

    # To draw digraph with matplotlib and save the plot
    '''
    plt.clf()
    plt_name = f'{tweet.id}'
    nx.draw_networkx(digraph, arrows = True, with_labels = False)
    limits = plt.axis('off')
    plt.draw()
    plt.savefig(plt_name)
    print(f'Plot saved as {plt_name}.png')
    '''
    return







def get_friends_list(user_id, cursor):

    try:
        #oauth = api.auth.oauth # OAuth1Session object
        friend_ids_list = []
        next_cursor, previous_cursor, friends = api_secondary.GetFriendsPaged(user_id = user_id, cursor = cursor, count = 200)

        for friend in friends:

            friend_ids_list.append(friend.id)

        return friend_ids_list, next_cursor
    except AttributeError as e:
        print(e)
        raise tweepy.RateLimitError("Rate limit on friends/list request, waiting on ids requests")








'''
# Takes the tweet id, retrieves existing full digraph and list of retweets from storage
# Finds follower relationships between the retweeters
# Draw an edge from A to B if B follows A
# Save full digraph for the tweet in storage every 5 times follower requests are made
# Save again
'''

def build_network(tweet):

    time.sleep(10) #to make sure that the network is built after the new retweets are requested
    digraph = nx.DiGraph()
    tweet_path = os.path.join(storage_path, f'{tweet.id}.pkl')
    storage ={}
    # Even if the tweet is new, 'main thread' will have initialized the storage file_name
    with storage_lock:
        with open(tweet_path, 'rb') as f:
            storage = pickle.load(f)


    existing_graph = storage['digraph']
    list_of_retweets = storage['retweets']
    next_id_pos = storage['next_id_pos'] # this is 0 when the graph is new


    # if the existing graph is empty, make a graph with the first node being the OP
    if existing_graph == {}:
        print(f"    Making new digraph for {tweet.id}") #debug
        digraph = nx.DiGraph()
        digraph.add_node(tweet.user.id)
        existing_graph = nx.to_dict_of_dicts(digraph) #the existing_graph is now not an empty string
        # we do not need to check who the original poster follows because we are only concerned with how the

    #

    digraph = nx.from_dict_of_dicts(existing_graph, create_using = nx.DiGraph())
    print(f"    Existing digraph contains {len(digraph.nodes())} nodes") #debug
    list_of_user_ids = [tweet.user.id]

    for retweet in list_of_retweets:
        list_of_user_ids.append(retweet.user.id)

    digraph.add_nodes_from(list_of_user_ids) # it doesnt matter if the nodes already exist in the graph

    for enumerator, source_id in enumerate(list_of_user_ids[next_id_pos:], start = next_id_pos): #resume graph-building process at the previous position
        print(f"    {enumerator}/{len(list_of_user_ids)} Checking followers of {source_id} for retweets")


        #
        try:
            api_string = "/friends/ids"
            for friend_id in limit_handled_friend(tweepy.Cursor(api.friends_ids, user_id = source_id).items(), api_string):
                if digraph.has_node(friend_id):
                    digraph.add_edge(friend_id, source_id)

        #this exception is raised when the user has protected tweets
        except tweepy.TweepError:
            print("Failed to run the command on that user, Skipping...")
        except FirstCursorRateError:
                api_string = "/friends/list"
                print("     Rate limit on friends/ids requests, making friends/list requests")
                cursor = -1
                while(True):
                    try:
                        friend_ids_list, cursor = get_friends_list(user_id = source_id, cursor = cursor) #outputs list of ids and next cursor

                        for friend_id in friend_ids_list:
                            if digraph.has_node(friend_id):
                                digraph.add_edge(friend_id, source_id)

                        if cursor == 0:
                            break #cursor value of 0 indicates that there are no further requests to be made

                    except twitter.TwitterError:
                        if cursor != 0 and cursor != -1: # 0 means that the last page was sent, -1 means that the request for the first page did not go through
                            countdown(api_string)

                        else:
                            print(" Rate limit on friends/lists requests, making friends/ids requests")

                            api_string = "/friends/ids"
                            for friend_id in limit_handled(tweepy.Cursor(api.friends_ids, user_id = source_id).items(), api_string):
                                if digraph.has_node(friend_id):
                                    digraph.add_edge(friend_id, source_id)
                            break

        # save after every user is processed
        with storage_lock:
            with open(tweet_path, 'rb') as f:
                storage = pickle.load(f)
            dict_dict = nx.to_dict_of_dicts(digraph)
            storage['digraph'] = dict_dict
            storage['next_id_pos'] = enumerator
            print(f"{enumerator} users processed. Saving graph-building progress...")
            with open(tweet_path, 'wb') as f:
                pickle.dump(storage, f)



    # To save digraph as .gml file for Gephi
    file_name = f'full{tweet.id}.gml'
    current_path = os.path.abspath("")
    path = os.path.join(current_path, 'gmlGraphs')
    path = os.path.join(path, file_name)
    nx.write_gml(digraph, path)
    print("File saved as " + file_name) #debug
    '''
    # To draw digraph with matplotlib and save the plot
    plt.clf()
    plt_name = f'{tweet.id}'
    nx.draw_networkx(digraph, arrows = True, with_labels = False)
    limits = plt.axis('off')
    plt.draw()
    plt.savefig(plt_name)
    print(f'Plot saved as {plt_name}.png')
    '''

    orient_graph(tweet)
    return



"""
# Takes a list of tweet ids and


"""

def main(list_of_ids):
    print(f"Running main on {len(list_of_ids)} original statuses") #debug


    storage = {}

    for id in list_of_ids:
        tweet_path = os.path.join(storage_path, f'{id}.pkl')
        try:
            with storage_lock:
                with open(tweet_path, 'rb') as f:
                    storage = pickle.load(f)

                print(f"{id} is a previously analyzed tweet") #debug
        except FileNotFoundError as e:
            storage = {}
            storage['retweets'] = []
            storage['digraph'] = {}
            storage['oriented'] = {}
            storage['next_id_pos'] = 0
            with open(tweet_path, 'wb') as f:
                pickle.dump(storage, f)
            print(f"{id} is a new tweet") #debug

            ## print(f"Storage contains data on {len(storage)} tweets")#debug
            # Read file containing a dictionary
            ## Where dict[tweet_id]['retweets'] contains a list of retweet objects
            ## and dict[tweet_id]['digraph'] contains a digraph representated as a dictionary of dictionaries

            #Handles both new tweets and tweets for which it already has data
    while(True):


        list_of_objects = []
        while True:
            # First get all tweet objects
            api_string = '/statuses/lookup'
            list_of_objects = []
            try:
                list_of_objects = api.statuses_lookup(id_ = list_of_ids) #GET /statuses/lookup
                #print(f"Ran {api_string} successfully") #debug
                #   Returns fully-hydrated Tweet object for up to 100 Tweets per request
                    ##   https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-lookup
                    ##  900(user)/300(app) requests in a 15-min window
                break
            except tweepy.RateLimitError as e:
                print("Rate limt exceeded while gathering list of tweet objects ")
                print(e)
                countdown(api_string)



        print("Checking retweet count of all tweets at " + datetime.datetime.now().strftime('%b %d, %Y at %H:%M:%S')) #debug
        queue_put = False
        for tweet in list_of_objects:
            tweet_path = os.path.join(storage_path, f'{tweet.id}.pkl')

            with storage_lock:
                with open(tweet_path, 'rb') as f:
                    storage = pickle.load(f)

                new_count = tweet.retweet_count
                old_rt_list = storage['retweets']
                next_id_pos = storage['next_id_pos']

                if len(storage['retweets']) > 0:
                    old_count = old_rt_list[-1].retweeted_status.retweet_count
                else:
                    old_count = 0
                #only check tweet if it has a certain number of more tweets

                if new_count > (old_count) or old_count == 0:
                    '''
                    #and there isnt already a retweet getter task running for that tweet
                    '''
                    print(f"    Putting {tweet.id} in queues")


                    retweet_queue.put(tweet)
                    time.sleep(1)
                    builder_queue.put(tweet)
                    queue_put = True
                elif next_id_pos <= len(old_rt_list):
                    print(f"    Resuming Graph-building for {tweet.id}")
                    queue_put = True
                    builder_queue.put(tweet)

        if not queue_put:
            print(" No Tweets had new retweets")

        time.sleep(main_sleep_time) #wait a bit so that we can recheck retweet count a maximum of 900 times in 15 min






def retweet_threader():
    while True:
        if not retweet_queue.empty():
            get_more_retweets(retweet_queue.get())
            retweet_queue.task_done()
        time.sleep(1)

def builder_threader():
    while True:
        if not builder_queue.empty():
            build_network(builder_queue.get())
            builder_queue.task_done()
        time.sleep(1)

def main_threader(list_of_ids):
    main(list_of_ids)





if __name__ == '__main__':

    print("Starting...")


#old
    #https://twitter.com/AyoCaesar/status/1084526697129656320
    #https://twitter.com/dril/status/1073288061222416384
    #https://twitter.com/ResistanceHole/status/1072537589066973184
    #https://twitter.com/JamilahLemieux/status/1072565296500801541
    # https://twitter.com/J_Appleyard/status/1062714222663081984
    # https://twitter.com/brendonfacts/status/1064292313797668869
    # https://twitter.com/lxrdxyz/status/1064397964238573568
    # https://twitter.com/TFerrara2/status/1064025163342200832
    # https://twitter.com/maddymcconnon88/status/1063959627761680386
    # https://twitter.com/pcyIine/status/1067471643113594887
    # https://twitter.com/IAmMekoB/status/1067605231817670657
    # https://twitter.com/KumarsSalehi/status/1071870040901742592
    # https://twitter.com/PhilosophyTube/status/1071873259644354560


 ####
    #https://twitter.com/uppittynegress/status/1084813938892697600
    #https://twitter.com/BootsRiley/status/1085069992779866112
    #https://twitter.com/ejhchess/status/1084935728050651136
    #https://twitter.com/Realaustinpower/status/7051823472
    #https://twitter.com/BBCWorld/status/1089604257475715077
    #https://twitter.com/BBCNews/status/1089932469154004992
#https://twitter.com/Anderso1A/status/706458719043760128
#https://twitter.com/BBCSport/status/1092102916876382210
#https://twitter.com/BBCWorld/status/1095446492997976068
#https://twitter.com/BBCWorld/status/1095445398666256384
#https://twitter.com/BenMBland/status/1097407064970878976
#https://twitter.com/Sunni_Tz/status/1097547656761626627
#https://twitter.com/AyoCaesar/status/1097978018537066498
    tid = 1095446492997976068
    list_of_ids = [tid, 1097407064970878976, 1097547656761626627, 1097978018537066498] #must not exceed 100 tweets

    main_thread = threading.Thread(target = main_threader, args = (list_of_ids,))



    print("Starting threads")

    main_thread.start()

    retweet_thread = threading.Thread(target = retweet_threader)

    retweet_thread.start()
    time.sleep(1)
    builder_thread = threading.Thread(target = builder_threader)

    builder_thread.start()
