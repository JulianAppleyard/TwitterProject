# TwitterProject
Both applications were written for Python 3.7.3 and use several libraries including
- networkx
- tweepy
- pickle
- requests
- twitter
- threading
and other, more common libraries like time and datetime


threadedRetweetGrapher.py is Application A

This can be run as normal from the command line. It only analyzes the tweet IDs written in the list in the main function at the bottom of the source code. It will produce .pkl files in the subdirectory /storage/ and .gml files in the subdirectory /gmlGraphs/. Make sure these subdirectories exist in the directory in which the program is run.

SnaFunctions.py is Application B
This can be run as normal from the command line. It asks the user to enter a tweet ID. This tweet ID must be one which has already been processed by Application A. It needs the .pkl for that tweet ID to exist and contain an oriented version of the graph. It will also produce a .gml file in the /gmlGraphs/ subdirectory.

