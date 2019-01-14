#julian J_Appleyard
#january 13th 2019

import pickle
import os.path





"""
A short script for taking old format storage and putting it into a new format


The old format was a single file 'storage.pkl' containing dictionaries of all tweets and the data associated with them
The new format is seperate files for each tweet in a sudirectory of the project
"""

old_storage = {}

with open('storage.pkl', 'rb') as f:
    old_storage = pickle.load(f)

current_path = os.path.abspath("")


for id in old_storage:
    file_name = f'{id}.pkl'
    new_storage = {}

    new_storage['retweets'] = old_storage[id]['retweets']
    new_storage['digraph'] = old_storage[id]['digraph']
    new_storage['oriented'] = {}

    path = os.path.join(current_path, 'storage')
    path = os.path.join(path, file_name)
    with open(path, 'wb') as f:
        pickle.dump(new_storage, f)
