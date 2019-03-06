
import pickle
import networkx as nx
import os.path
#longest induced path is maximum shortest path




storage_path = os.path.join(os.path.abspath(""), 'storage')


shortest_path(node_a, node_b):
    shortest = 0


    return shortest





longest_induced_path(tweet_id):

    tweet_path = os.path.join(storage_path, f'{tweet_id}.pkl')
    with open(tweet_path, 'rb') as f:
        storage = pickle.load(f)

    oriented_dict_dict = storage['oriented']

    digraph_o = nx.from_dict_of_dicts(oriented_dict_dict, create_using = nx.DiGraph())

    longest = 0
    for node1 in digraph_o:

        for node2 in digraph_o:
            if node1 == node2 or has_path(digraph_o, node1, node2) == False: break

            shortest_1_2 = shortest_path(node1, node2)
            if  shortest_1_2 > longest:
                longest = shortest_1_2

    return longest
