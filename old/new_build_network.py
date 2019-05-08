





import requests
import json








def get_friends_list(user_id, cursor):

    url = f"https://api.twitter.com/1.1/friends/list.json?&user_id={user_id}cursor={cursor}&count=200&skip_status=true&include_user_entities=false"
    response_json = requests.get(url, auth = auth)

    response = json.loads(response_json) #turns the response string into a python dictioanry


    next_cursor = response.next_cursor

    return friend_ids_list, next_cursor






def build_network(tweet):

    time.sleep(10) #to make sure that the network is built after the new retweets are requested
    digraph = nx.Digraph()
    tweet_path = os.path.join(storage_path, f'{tweet.id}.pkl')
    storage ={}
    with storage_lock:
        with open(tweet_path, 'rb') as f:
            storage = pickle.load(f)


    existing_graph = storage['digraph']
    list_of_retweets = storage['retweets']
    next_id_pos = storage['next_id_pos'] # this is 0 when the graph is new


    # if there is no existing graph, make a graph with the first node being the OP
    if existing_graph = {}:
        print(f"    Making new digraph for {tweet.id}") #debug
        digraph = nx.Digraph()
        digraph.add_node(tweet.id)
        existing_graph = nx.to_dict_of_dicts(digraph) #the existing_graph is now not an empty string
        # we do not need to check who the original poster follows because we are only concerned with how the

    # if the graph is not empty, add edges from
    if existing_graph != {}: #
        digraph = nx.from_dict_of_dicts(existing_graph, create_using = nx.DiGraph())
        print(f"    Existing digraph contains {len(digraph.nodes())} nodes") #debug
        list_of_user_ids = []

        for retweet in list_of_retweets:
            list_of_user_ids.append(retweet.user.id)

        digraph.add_nodes_from(list_of_user_ids) # it doesnt matter if the nodes already exist in the graph

        enumerator = next_id_pos
        for enumerator, source_id in enumerate(list_of_user_ids[next_id_pos:]): #resume graph-building process at the previous position
            print(f"    {enumerator}/{len(digraph.nodes()-1)} Checking followers of {source_id} for retweets")

            try:
                for friend_id in limit_handled_friend(tweepy.Cursor(api.friends_ids, user_id = source_id).items(), api_string):
                    if digraph.has_node(friend_id):
                        digraph.add_edge(friend_id, source_id)

            except FirstCursorRateError:
                cursor = -1
                while(True):
                    friend_ids_list, cursor = get_friends_list(user_id = source_id, cursor = cursor) #outputs list of ids and next cursor

                    for friend_id in friend_ids_list:

                        if digraph.has_node(friend_id):
                            digraph.add_edge(friend_id, source_id)

                    if cursor == 0:
                        break #cursor value of 0 indicates that there are no further requests to be made

            # save after every user is processed
            with storage_lock:
                with open(tweet_path, 'rb') as f:
                    storage = pickle.load(f)
                print(f"{counter} edges added. Saving digraph...")
                dict_dict = nx.to_dict_of_dicts(digraph)
                storage['digraph'] = dict_dict
                storage['next_id_pos'] = enumerator
                with open(tweet_path, 'wb') as f:
                    pickle.dump(storage, f)
