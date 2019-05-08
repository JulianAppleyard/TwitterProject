
import pickle
import time
import networkx as nx
import os.path
import math
import random
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
#longest induced path is maximum shortest path


# All assume no self-loops

STORAGE_PATH = os.path.join(os.path.abspath(""), 'storage')
TWEET_ID = 1084813938892697600








def longest_induced_path(tweet_id = TWEET_ID):

    tweet_path = os.path.join(STORAGE_PATH, f'{tweet_id}.pkl')
    with open(tweet_path, 'rb') as f:
        storage = pickle.load(f)

    oriented_dict_dict = storage['oriented']

    digraph_o = nx.from_dict_of_dicts(oriented_dict_dict, create_using = nx.DiGraph())
    largest_component = max(nx.weakly_connected_components(digraph_o), key=len)
    digraph_o = digraph_o.subgraph(largest_component)

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



    return longest


"""
    Uses pseudocode from: Brandes' Algorithm from (2001)"A Faster Algorithm for Betweeness Centrality"

    Then normalizes the betweenness centrality to between 0 and 1
"""



def betweenness_centrality(tweet_id = TWEET_ID):

    tweet_path = os.path.join(STORAGE_PATH, f'{tweet_id}.pkl')
    with open(tweet_path, 'rb') as f:
        storage = pickle.load(f)

    digraph = nx.from_dict_of_dicts(storage['oriented'], create_using = nx.DiGraph())
    # Only take the largest connected component
    largest_component = max(nx.weakly_connected_components(digraph), key=len)
    digraph = digraph.subgraph(largest_component)
    num_nodes = nx.number_of_nodes(digraph)
    print("Nodes in largest weakly connected subgraph: ", num_nodes)
    num_edges = nx.number_of_edges(digraph)
    print("Edges in largest wekaly connected subgraph: ", num_edges)
    betweenness_dict = {}

    # All betweenness values are initiially 0
    for vertex in digraph:
        betweenness_dict[vertex] = 0.0

    for s in digraph:
        stack = deque() # Empty stack (LIFO) for each vertex looped
        # Will use append() to push to the right side of the stack
        # will use pop() to pop from the right side of the stack

        p = {} # keys are vertices, values are lists
        sigma = {} # keys are vertices, values are integers
        d = {} # keys are vertices, values are integers

        for w in digraph:
            p[w] = []
        for t in digraph:
            sigma[t] = 0.0
            d[t] = -1

        sigma[s] = 1
        d[s] = 0.0
        queue = deque() # This represents a FIFO queue data structure
        # will use append() to enqueue to the right end of the queue
        # will use popleft() to dequeue the item on the leftmost side

        queue.append(s) # First in will be on the left
        while len(queue) > 0:
            v = queue.popleft() # first out will be on the left
            stack.append(v)

            for w in digraph.neighbors(v):
                # w found for the first time?
                if d[w] < 0:
                    queue.append(w)
                    d[w] = d[v] + 1
                # shortest path to w via v?
                if d[w] == d[v] + 1:
                    sigma[w] = sigma[w] + sigma[v]
                    p[w].append(v)


        """Accumulation"""
        delta = {}
        betweenness_dict[s] = betweenness_dict[s] + (len(stack) -1) #number of times s is a source
        for v in digraph:
            delta[v] = 0.0
        while len(stack) > 0:
            w = stack.pop()
            for v in p[w]:
                delta[v] = delta[v] + ((sigma[v]/sigma[w])*(1 + delta[w]))
            if w != s:
                betweenness_dict[w] = betweenness_dict[w] + delta[w] +1




    return betweenness_dict


"""
    Uses NetworkX built-in betweenness centrality function which also uses the abovementioned algorithm



    Uses pseudocode from: (Brandes 2001)
"""

def networkx_betweenness_centrality(tweet_id = TWEET_ID):

    tweet_path = os.path.join(STORAGE_PATH, f'{tweet_id}.pkl')
    with open(tweet_path, 'rb') as f:
        storage = pickle.load(f)

    oriented_dict_dict = storage['oriented']
    digraph = nx.from_dict_of_dicts(oriented_dict_dict, create_using = nx.DiGraph())
    # Only take the largest connected component
    largest_component = max(nx.weakly_connected_components(digraph), key=len)
    digraph = digraph.subgraph(largest_component)

    betweenness_dict = nx.betweenness_centrality(digraph)
    highest_val = 0
    highest_id = 0
    #print(betweenness_dict)


    return betweenness_dict



"""



"""
def k_path_centrality(tweet_id = TWEET_ID):


    alpha = 0.2
    k_path_dict = {} # a dictionary where the key is the vertex and the value is the k_path centrality

    tweet_path = os.path.join(STORAGE_PATH, f'{tweet_id}.pkl')
    with open(tweet_path, 'rb') as f:
        storage = pickle.load(f)

    digraph = nx.from_dict_of_dicts(storage['oriented'], create_using = nx.DiGraph())
    # Only take the largest connected component
    largest_component = max(nx.weakly_connected_components(digraph), key=len)
    digraph = digraph.subgraph(largest_component)

    num_nodes = nx.number_of_nodes(digraph)
    print("Nodes in largest weakly connected subgraph: ", num_nodes)
    num_edges = nx.number_of_edges(digraph)
    print("Edges in largest weakly connected subgraph: ", num_edges)
    k = round(math.log(num_nodes+num_edges)) # from page 22 (section 4.5 of the paper) this is optimal k value for a given graph
    #this value needs to be rounded to be an integer

    print("k is: ",k)

    count = {} # a dictionary with the the key being the vertex id and the value being the number of times the vertex has been visited over all the random walks
    explored = {} #  (?) a dictionary with the key being the vertex id and the value being a boolean value indicating whether the vertex has been explored
    n = nx.number_of_nodes(digraph)
    for vertex in digraph:
        count[vertex] = 0
        explored[vertex] = False

        #stack starts as an empty set
    stack = deque() #append() to push pop() (no index) to pop
    t = 2*(k**2)*math.pow(n, 1-(2*alpha))*math.log(n)
    #print(f"t is {t}")

    i = 1
    while i <= t:
        """Simulate a message traversal from s containing l links"""
        s = random.choice(list(digraph)) # choose an a vertex randomly from the graph
        l = random.randint(1, k) #choose an integer walk length from between 1 and k (inclusive)

        explored[s] = True
        stack.append(s)
        j = 1
        flag_u = True
        while j <= 1 and flag_u:
            flag_u = False # flag_u is true when there is a u where (s, u) is a valid edge and u has not been explored
            u_list = []
            for u in digraph:
                if digraph.has_edge(s, u) and explored[u] == False:

                    flag_u = True
                    u_list.append(u)

            if flag_u == False: continue

            v = random.choice(u_list) # "with probability proportional to 1/(weight function(s,v))" but our graph is unweighted so that weight is always 1
            explored[v] = True
            stack.append(v)
            count[v] += 1
            s = v
            j += 1

        """ reinitialize Explored[v] to false"""
        while len(stack) != 0:
            v = stack.pop()
            explored[v] = False

        i += 1

    for vertex in digraph:
        k_path_dict[vertex] = k * n * (count[vertex]/t)



    return k_path_dict, k


def main():
    # Takes user input removing all spaces,
    # Expects an integer value corresponding to one of the tweets in storage
    flag = True
    k = 0
    while flag:
        try:

            user_input = int(input('Enter ID of tweet to be analyzed: ').strip())

            tweet_path = os.path.join(STORAGE_PATH, f'{user_input}.pkl')
            with open(tweet_path, 'rb') as f:
                storage = pickle.load(f)

            TWEET_ID= user_input


            #user_input = int(input('Enter k value (Recommended: PLACEHOLDER) for k path centrality analysis: '))


            flag = False # If the user enters good values, proceed with the calculations by breaking this loop

        except ValueError:
            print("Error: Not a valid value. Inputs must be integers.")
        except FileNotFoundError:
            print("Error: Tweet ID is not valid or does not exist in storage.")





    print("Computing longest induced path for the entire graph...")
    longest = longest_induced_path(tweet_id = TWEET_ID)
    print("Longest induced path is: ", longest)

    print("Computing betweenness centrality...")
    bet_dict = betweenness_centrality(tweet_id = TWEET_ID)


    maxBC = bet_dict[max(bet_dict, key = bet_dict.get)]

    minBC = bet_dict[min(bet_dict, key = bet_dict.get)]

    print("Highest betweenness centrality is ", maxBC)
    print("Lowest betweenness centrality is ", minBC)

    print("Computing NetworkX betweenness centrality...")
    nx_dict = networkx_betweenness_centrality(tweet_id = TWEET_ID)
    maxNX = nx_dict[max(nx_dict, key = nx_dict.get)]

    minNX = nx_dict[min(nx_dict, key = nx_dict.get)]

    print(f"Computing k-path centrality...")
    k_dict,k = k_path_centrality(tweet_id = TWEET_ID)
    #print(k_dict)
    maxk = k_dict[max(k_dict, key = k_dict.get)]
    mink = k_dict[min(k_dict, key = k_dict.get)]

    print(f"Highest {k}-path centrality is ", maxk)
    print(f"Lowest {k}-path centrality is ", mink)



    print("Saving to file...")
    storage = {}
    with open(tweet_path, 'rb') as f:
        storage = pickle.load(f)

    digraph = nx.from_dict_of_dicts(storage['oriented'], nx.DiGraph())
    # Only take the largest connected component
    largest_component = max(nx.weakly_connected_components(digraph), key=len)
    digraph = digraph.subgraph(largest_component)

    digraph.graph['linduced'] = longest
    digraph.graph['kvalue'] = k


    #bc_values = [] #array of all betweenness centrality values in graph

    for node in digraph:
        digraph.nodes[node]['kpath'] = k_dict[node]

        digraph.nodes[node]['bc'] = bet_dict[node]


        digraph.nodes[node]['nxbc'] = nx_dict[node]

        #bc_values.append(bet_dict[node])

        digraph.nodes[node]['normalizedbc'] = (bet_dict[node]-minBC)/(maxBC-minBC)
        digraph.nodes[node]['normalizedkpath'] = (k_dict[node]-mink)/(maxk-mink)
        digraph.nodes[node]['normalizednx'] = (nx_dict[node]-minNX)/(maxBC-minNX)



        #make new gml
    file_name = f'analyzed{TWEET_ID}.gml'
    current_path = os.path.abspath("")
    path = os.path.join(current_path, 'gmlGraphs')
    path = os.path.join(path, file_name)
    nx.write_gml(digraph, path)
    print("File saved as " + file_name)

    """
    plt.clf()

    bc_values.sort()
    bc_percent = []
    for i,val in enumerate(bc_values):

        bc_percent.append(np.percentile(bc_values, bc_values[i]))

    plt_name = f'bcpercentile{TWEET_ID}'
    plt.xlabel('Betweeness Centrality')
    plt.ylabel('Percentile')
    plt.suptitle('Percentile Distirbution of Betweenness Centrality Values')

    plt.plot(bc_values, bc_percent, marker = '.', linestyle = 'none', color = 'b')
    axes = plt.gca()


    plt.savefig(plt_name)
    print("File saved as " + plt_name)
    """





    print("DONE")
if __name__ == '__main__':
    main()
