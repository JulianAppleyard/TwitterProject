import pickle
import networkx as nx
import os.path
import math
import random
from collections import deque




# Assumes no self-loops


STORAGE_PATH = os.path.join(os.path.abspath(""), 'storage')


#def betweenness_centrality(tweet_id)

tweet_id = 1084813938892697600 #example. comment out

tweet_path = os.path.join(STORAGE_PATH, f'{tweet_id}.pkl')

with open(tweet_path, 'rb') as f:
    storage = pickle.load(f)

digraph = nx.from_dict_of_dicts(storage['digraph'], create_using = nx.DiGraph())


"""
Brandes' Algorithm from (2001)"A Faster Algorithm for Betweeness Centrality"
"""

betweenness_dict = {}

# All betweenness values are initiially 0
for vertex in digraph:
    betweenness_dict[vertex] = 0

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
        sigma[t] = 0
        d[t] = -1

    sigma[s] = 1
    d[s] = 0
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
    delta = {}
    for v in digraph:
        delta[v] = 0
    while len(stack) > 0:
        w = stack.pop()
        for v in p[w]:
            delta[v] = delta[v] + ((sigma[v]/sigma[w])*(1 + delta[w]))
        if w != s:
            betweenness_dict[w] = betweenness_dict[w] + delta[w]
print(betweenness_dict)
