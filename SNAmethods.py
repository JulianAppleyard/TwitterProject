
import pickle
import networkx as nx
import os.path
import math
import random
from collections import deque
#longest induced path is maximum shortest path




STORAGE_PATH = os.path.join(os.path.abspath(""), 'storage')
TWEET_ID = 1084813938892697600








def longest_induced_path(tweet_id = 1084813938892697600):

    tweet_path = os.path.join(STORAGE_PATH, f'{tweet_id}.pkl')
    with open(tweet_path, 'rb') as f:
        storage = pickle.load(f)

    oriented_dict_dict = storage['oriented']

    digraph_o = nx.from_dict_of_dicts(oriented_dict_dict, create_using = nx.DiGraph())

    longest = 0
    for node1 in digraph_o:

        for node2 in digraph_o:
            if node1 == node2 or nx.has_path(digraph_o, node1, node2) == False: continue #this ensures that path lengths of zero or undefined are not considered

            paths_generator = nx.shortest_simple_paths(digraph_o, node1, node2) # the nx function returns a generator of paths
            # each path is the list of nodes in the order in which they appear in the path

            shortest_1_2 = next(paths_generator)
            #the length of any one of these paths is the number of nodes minus 1 (i.e. the number of edges)
            path_length = (len(shortest_1_2)-1)
            if path_length > longest:
                longest = path_length
    print(longest)
    return longest


def betweenness_centrality(tweet_id = 1097978018537066498):

    tweet_path = os.path.join(STORAGE_PATH, f'{tweet_id}.pkl')
    with open(tweet_path, 'rb') as f:
        storage = pickle.load(f)

    oriented_dict_dict = storage['oriented']
    digraph_o = nx.from_dict_of_dicts(oriented_dict_dict, create_using = nx.DiGraph())

    betweenness_dict = nx.betweenness_centrality(digraph_o)
    highest_val = 0
    highest_id = 0
    #print(betweenness_dict)
    for node in betweenness_dict:
        if betweenness_dict[node] >= highest_val:
            highest_val = betweenness_dict[node]
            highest_id = node

    print(highest_id)
    print("With centrality of ", highest_val)

if __name__ == '__main__':
    longest_induced_path()
