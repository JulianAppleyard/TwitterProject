import pickle
import networkx as nx
import os.path
import math
import random
from collections import deque


# This was produced from pseudocode for Randomized-Approximated k-path centrality in (Alakoon 2011) 

# Assumes no self-loops


STORAGE_PATH = os.path.join(os.path.abspath(""), 'storage')
TWEET_ID = 1084813938892697600

k = 5 #must be at least 1

alpha = random.uniform(-0.5, 0.5) #this function is inclusive
k_path_dict = {} # a dictionary where the key is the vertex and the value is the k_path centrality

tweet_path = os.path.join(STORAGE_PATH, f'{TWEET_ID}.pkl')
# Do I want data stored in a different place or in the same pickled dictionary object?
## I think probably in a different place because the dictionaries are big as it is

with open(tweet_path, 'rb') as f:
    storage = pickle.load(f)


digraph = nx.from_dict_of_dicts(storage['digraph'], create_using = nx.DiGraph())

count = {} # a dictionary with the the key being the vertex id and the value being the number of times the vertex has been visited over all the random walks
explored = {} #  (?) a dictionary with the key being the vertex id and the value being a boolean value indicating whether the vertex has been explored
n = nx.number_of_nodes(digraph)
for vertex in digraph:
    count[vertex] = 0
    explored[vertex] = False

    #stack starts as an empty set
stack = deque() #append() to push pop() (no index) to pop
t = 2*(k**2)*math.pow(n, 1-(2*alpha))*math.log(n)
print(f"t is {t}")

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

print(k_path_dict)
