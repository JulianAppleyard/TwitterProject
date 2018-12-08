import tweepy #http://docs.tweepy.org/en/v3.6.0/


import networkx as nx


import json
import time
import asyncio


access_token= "1043132884759072769-aqQYY7XQ2Rlj5CdXdLRgv0I3us3Dxs"
access_token_secret = "hIdttcfhoLqvoNVVvs7myVocBlVoKisqGgonqrk6WFXAh"
consumer_key= "YAUrjz6OEkKtVsnNuG0ZfdI7t"
consumer_secret= "vs6i2CdSphMn9MXoNg2azdSMqL0fzjQxIpLYXud3CajqFj8xZw"


#authetication requests
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


#create api variable
api = tweepy.API(auth)

try:
	while True: api.show_friendship(source_screen_name = 'JulianAppleya14', target_screen_name = 'BBCWorld')
except tweepy.RateLimitError as e:
	print(e)

	rate_status = api.rate_limit_status()
	print(rate_status)
	reset_time = rate_status['resources']['friendships']['/friendships/show']['reset']
	print(reset_time - time.time())


'''
[{'message': 'Rate limit exceeded', 'code': 88}]
{'rate_limit_context': {'access_token': '1043132884759072769-aqQYY7XQ2Rlj5CdXdLRgv0I3us3Dxs'},
'resources': {
	'lists': {
		'/lists/list': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/lists/memberships': {'limit': 75, 'remaining': 75, 'reset': 1542559625},
		'/lists/subscribers/show': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/lists/members': {'limit': 900, 'remaining': 900, 'reset': 1542559625},
		'/lists/subscriptions': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/lists/show': {'limit': 75, 'remaining': 75, 'reset': 1542559625},
		'/lists/ownerships': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/lists/subscribers': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
		'/lists/members/show': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/lists/statuses': {'limit': 900, 'remaining': 900, 'reset': 1542559625}
		},
	'application':
		{'/application/rate_limit_status': {'limit': 180, 'remaining': 171, 'reset': 1542559143}},
	'mutes':
		{'/mutes/users/list': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/mutes/users/ids': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'live_video_stream':
        {'/live_video_stream/status/:id': {'limit': 1000, 'remaining': 1000, 'reset': 1542559625}},
	'friendships':
		{'/friendships/outgoing': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/friendships/list': {'limit': 200, 'remaining': 200, 'reset': 1542559625},
		'/friendships/no_retweets/ids': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/friendships/lookup': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/friendships/incoming': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/friendships/show': {'limit': 180, 'remaining': 0, 'reset': 1542558986}},
	'guide': {'/guide': {'limit': 180, 'remaining': 180, 'reset': 1542559625}},
	'auth': {'/auth/csrf_token': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'blocks':
		{'/blocks/list': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/blocks/ids': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'geo':
		{'/geo/similar_places': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/geo/id/:place_id': {'limit': 75, 'remaining': 75, 'reset': 1542559625},
		'/geo/reverse_geocode': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/geo/search': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'users':
		{'/users/report_spam': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/users/contributors/pending': {'limit': 2000, 'remaining': 2000, 'reset': 1542559625},
		'/users/show/:id': {'limit': 900, 'remaining': 900, 'reset': 1542559625},
		'/users/search': {'limit': 900, 'remaining': 900, 'reset': 1542559625},
		'/users/suggestions/:slug': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/users/contributees/pending': {'limit': 200, 'remaining': 200, 'reset': 1542559625},
		'/users/derived_info': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/users/profile_banner': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
		'/users/suggestions/:slug/members': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/users/lookup': {'limit': 900, 'remaining': 900, 'reset': 1542559625},
		'/users/suggestions': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'followers':
		{'/followers/ids': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/followers/list': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'collections':
		{'/collections/list': {'limit': 1000, 'remaining': 1000, 'reset': 1542559625},
		'/collections/entries': {'limit': 1000, 'remaining': 1000, 'reset': 1542559625},
		'/collections/show': {'limit': 1000, 'remaining': 1000, 'reset': 1542559625}},
	'statuses':
		 {'/statuses/retweeters/ids': {'limit': 75, 'remaining': 75, 'reset': 1542559625},
		 '/statuses/retweets_of_me': {'limit': 75, 'remaining': 75, 'reset': 1542559625},
		 '/statuses/home_timeline': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		 '/statuses/show/:id': {'limit': 900, 'remaining': 900, 'reset': 1542559625},
		 '/statuses/user_timeline': {'limit': 900, 'remaining': 900, 'reset': 1542559625},
		 '/statuses/friends': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		 '/statuses/retweets/:id': {'limit': 75, 'remaining': 75, 'reset': 1542559625},
		 '/statuses/mentions_timeline': {'limit': 75, 'remaining': 75, 'reset': 1542559625},
		 '/statuses/oembed': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
		 '/statuses/lookup': {'limit': 900, 'remaining': 900, 'reset': 1542559625}},
	 'custom_profiles':
	 	 {'/custom_profiles/list': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
	 	 '/custom_profiles/show': {'limit': 180, 'remaining': 180, 'reset': 1542559625}},
	 'webhooks':
	 	 {'/webhooks/subscriptions/direct_messages': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
	 	 '/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
 	 'contacts':
 	 	{'/contacts/uploaded_by': {'limit': 300, 'remaining': 300, 'reset': 1542559625},
 	 	'/contacts/users': {'limit': 300, 'remaining': 300, 'reset': 1542559625},
 	 	'/contacts/addressbook': {'limit': 300, 'remaining': 300, 'reset': 1542559625},
 	 	'/contacts/users_and_uploaded_by': {'limit': 300, 'remaining': 300, 'reset': 1542559625},
 	 	'/contacts/delete/status': {'limit': 300, 'remaining': 300, 'reset': 1542559625}},
 	'i':
 		 {'/i/config': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
 	'tweet_prompts':
 		{'/tweet_prompts/report_interaction': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
		'/tweet_prompts/show': {'limit': 180, 'remaining': 180, 'reset': 1542559625}},
	'moments':
		{'/moments/statuses/update': {'limit': 5, 'remaining': 5, 'reset': 1542559625},
		'/moments/permissions': {'limit': 300, 'remaining': 300, 'reset': 1542559625}},
	'help':
		{'/help/tos': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/help/configuration': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/help/privacy': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/help/settings': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/help/languages': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
		'feedback': {'/feedback/show/:id': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
		'/feedback/events': {'limit': 1000, 'remaining': 1000, 'reset': 1542559625}},
	'business_experience':
		{'/business_experience/dashboard_settings/destroy': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
		'/business_experience/dashboard_features': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
		'/business_experience/keywords': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
		'/business_experience/dashboard_settings/update': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
		'/business_experience/dashboard_settings/show': {'limit': 450, 'remaining': 450, 'reset': 1542559625}},
	'graphql&POST':
		 {'/graphql&POST': {'limit': 2500, 'remaining': 2500, 'reset': 1542559625}},
	'friends':
	 	 {'/friends/following/ids': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
	 	 '/friends/following/list': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
	 	 '/friends/list': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
	 	 '/friends/ids': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	 'sandbox':
	 	{'/sandbox/account_activity/webhooks/:id/subscriptions': {'limit': 500, 'remaining': 500, 'reset': 1542559625}},
	 'drafts':
	 	{'/drafts/statuses/update': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
	 	'/drafts/statuses/destroy': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
	 	'/drafts/statuses/ids': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
	 	'/drafts/statuses/list': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
	 	'/drafts/statuses/show': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
	 	'/drafts/statuses/create': {'limit': 450, 'remaining': 450, 'reset': 1542559625}},
 	'direct_messages':
 		{'/direct_messages/sent': {'limit': 300, 'remaining': 300, 'reset': 1542559625},
 		'/direct_messages/broadcasts/list': {'limit': 60, 'remaining': 60, 'reset': 1542559625},
 		'/direct_messages/subscribers/lists/members/show': {'limit': 1000, 'remaining': 1000, 'reset': 1542559625},
 		'/direct_messages/mark_read': {'limit': 1000, 'remaining': 1000, 'reset': 1542559625},
 		'/direct_messages/subscribers/ids': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
 		'/direct_messages/sent_and_received': {'limit': 300, 'remaining': 300, 'reset': 1542559625},
 		'/direct_messages/broadcasts/statuses/list': {'limit': 60, 'remaining': 60, 'reset': 1542559625},
 		'/direct_messages': {'limit': 300, 'remaining': 300, 'reset': 1542559625},
 		'/direct_messages/subscribers/lists/members/ids': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
 		'/direct_messages/subscribers/show': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
 		'/direct_messages/broadcasts/show': {'limit': 60, 'remaining': 60, 'reset': 1542559625},
 		'/direct_messages/broadcasts/statuses/show': {'limit': 60, 'remaining': 60, 'reset': 1542559625},
 		'/direct_messages/subscribers/lists/list': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
 		'/direct_messages/show': {'limit': 300, 'remaining': 300, 'reset': 1542559625},
 		'/direct_messages/events/list': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
 		'/direct_messages/subscribers/lists/show': {'limit': 180, 'remaining': 180, 'reset': 1542559625},
 		'/direct_messages/events/show': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'media':
		{'/media/upload': {'limit': 500, 'remaining': 500, 'reset': 1542559625}},
	'traffic':
		{'/traffic/map': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'account_activity':
		{'/account_activity/all/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/account_activity/all/:instance_name/subscriptions': {'limit': 500, 'remaining': 500, 'reset': 1542559625},
		'/account_activity/direct_messages/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/account_activity/webhooks/:id/subscriptions/direct_messages/list': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/account_activity/webhooks/:id/subscriptions/all': {'limit': 500, 'remaining': 500, 'reset': 1542559625},
		'/account_activity/direct_messages/:instance_name/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/account_activity/webhooks/:id/subscriptions/all/list': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/account_activity/webhooks/:id/subscriptions/direct_messages': {'limit': 500, 'remaining': 500, 'reset': 1542559625},
		'/account_activity/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/account_activity/direct_messages/:instance_name/subscriptions': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/account_activity/webhooks/:id/subscriptions': {'limit': 500, 'remaining': 500, 'reset': 1542559625},
		'/account_activity/all/:instance_name/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'account':
		{'/account/login_verification_enrollment': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/account/update_profile': {'limit': 15, 'remaining': 15, 'reset': 1542559625},
		'/account/verify_credentials': {'limit': 75, 'remaining': 75, 'reset': 1542559625},
		'/account/settings': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'safety':
		{'/safety/detection_feedback': {'limit': 1000, 'remaining': 1000, 'reset': 1542559625}},
	'favorites': {'/favorites/list': {'limit': 75, 'remaining': 75, 'reset': 1542559625}},
	'device': {'/device/token': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'tweets':
		{'/tweets/stream/filter/rules': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
		'/tweets/stream/filter/:instance_name': {'limit': 50, 'remaining': 50, 'reset': 1542559625},
		'/tweets/search/:product/:label': {'limit': 1800, 'remaining': 1800, 'reset': 1542559625},
		'/tweets/search/:product/:instance/counts': {'limit': 900, 'remaining': 900, 'reset': 1542559625},
		'/tweets/stream/filter/rules/:instance_name/validation&POST': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
		'/tweets/stream/filter/rules/:instance_name&POST': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
		'/tweets/stream/filter/rules/:instance_name&DELETE': {'limit': 450, 'remaining': 450, 'reset': 1542559625},
		'/tweets/stream/filter/rules/:instance_name/:rule_id': {'limit': 450, 'remaining': 450, 'reset': 1542559625}},
	'saved_searches': {'/saved_searches/destroy/:id': {'limit': 15, 'remaining': 15, 'reset': 1542559625}, '/saved_searches/show/:id': {'limit': 15, 'remaining': 15, 'reset': 1542559625}, '/saved_searches/list': {'limit': 15, 'remaining': 15, 'reset': 1542559625}},
	'oauth': {'/oauth/invalidate_token': {'limit': 450, 'remaining': 450, 'reset': 1542559625}}, 'search': {'/search/tweets': {'limit': 180, 'remaining': 180, 'reset': 1542559625}},
	'trends': {'/trends/closest': {'limit': 75, 'remaining': 75, 'reset': 1542559625}, '/trends/available': {'limit': 75, 'remaining': 75, 'reset': 1542559625}, '/trends/place': {'limit': 75, 'remaining': 75, 'reset': 1542559625}},
	'live_pipeline': {'/live_pipeline/events': {'limit': 180, 'remaining': 180, 'reset': 1542559625}}}}



'''






















81.62387180328369

(py3) C:\Users\Julian\Documents\GitHub\TwitterProject>test.py
[{'message': 'Rate limit exceeded', 'code': 88}]
{'rate_limit_context': {'access_token': '1043132884759072769-aqQYY7XQ2Rlj5CdXdLRgv0I3us3Dxs'}, 'resources': {'lists': {'/lists/list': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/lists/memberships': {'limit': 75, 'remaining': 75, 'reset': 1542561591}, '/lists/subscribers/show': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/lists/members': {'limit': 900, 'remaining': 900, 'reset': 1542561591}, '/lists/subscriptions': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/lists/show': {'limit': 75, 'remaining': 75, 'reset': 1542561591}, '/lists/ownerships': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/lists/subscribers': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/lists/members/show': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/lists/statuses': {'limit': 900, 'remaining': 900, 'reset': 1542561591}}, 'application': {'/application/rate_limit_status': {'limit': 180, 'remaining': 173, 'reset': 1542560806}}, 'mutes': {'/mutes/users/list': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/mutes/users/ids': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'live_video_stream': {'/live_video_stream/status/:id': {'limit': 1000, 'remaining': 1000, 'reset': 1542561591}}, 'friendships': {'/friendships/outgoing': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/friendships/list': {'limit': 200, 'remaining': 200, 'reset': 1542561591}, '/friendships/no_retweets/ids': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/friendships/lookup': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/friendships/incoming': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/friendships/show': {'limit': 180, 'remaining': 0, 'reset': 1542560748}}, 'guide': {'/guide': {'limit': 180, 'remaining': 180, 'reset': 1542561591}}, 'auth': {'/auth/csrf_token': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'blocks': {'/blocks/list': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/blocks/ids': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'geo': {'/geo/similar_places': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/geo/id/:place_id': {'limit': 75, 'remaining': 75, 'reset': 1542561591}, '/geo/reverse_geocode': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/geo/search': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'users': {'/users/report_spam': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/users/contributors/pending': {'limit': 2000, 'remaining': 2000, 'reset': 1542561591}, '/users/show/:id': {'limit': 900, 'remaining': 900, 'reset': 1542561591}, '/users/search': {'limit': 900, 'remaining': 900, 'reset': 1542561591}, '/users/suggestions/:slug': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/users/contributees/pending': {'limit': 200, 'remaining': 200, 'reset': 1542561591}, '/users/derived_info': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/users/profile_banner': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/users/suggestions/:slug/members': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/users/lookup': {'limit': 900, 'remaining': 900, 'reset': 1542561591}, '/users/suggestions': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'followers': {'/followers/ids': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/followers/list': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'collections': {'/collections/list': {'limit': 1000, 'remaining': 1000, 'reset': 1542561591}, '/collections/entries': {'limit': 1000, 'remaining': 1000, 'reset': 1542561591}, '/collections/show': {'limit': 1000, 'remaining': 1000, 'reset': 1542561591}}, 'statuses': {'/statuses/retweeters/ids': {'limit': 75, 'remaining': 75, 'reset': 1542561591}, '/statuses/retweets_of_me': {'limit': 75, 'remaining': 75, 'reset': 1542561591}, '/statuses/home_timeline': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/statuses/show/:id': {'limit': 900, 'remaining': 900, 'reset': 1542561591}, '/statuses/user_timeline': {'limit': 900, 'remaining': 900, 'reset': 1542561591}, '/statuses/friends': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/statuses/retweets/:id': {'limit': 75, 'remaining': 73, 'reset': 1542560960}, '/statuses/mentions_timeline': {'limit': 75, 'remaining': 75, 'reset': 1542561591}, '/statuses/oembed': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/statuses/lookup': {'limit': 900, 'remaining': 900, 'reset': 1542561591}}, 'custom_profiles': {'/custom_profiles/list': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/custom_profiles/show': {'limit': 180, 'remaining': 180, 'reset': 1542561591}}, 'webhooks': {'/webhooks/subscriptions/direct_messages': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'contacts': {'/contacts/uploaded_by': {'limit': 300, 'remaining': 300, 'reset': 1542561591}, '/contacts/users': {'limit': 300, 'remaining': 300, 'reset': 1542561591}, '/contacts/addressbook': {'limit': 300, 'remaining': 300, 'reset': 1542561591}, '/contacts/users_and_uploaded_by': {'limit': 300, 'remaining': 300, 'reset': 1542561591}, '/contacts/delete/status': {'limit': 300, 'remaining': 300, 'reset': 1542561591}}, 'i': {'/i/config': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'tweet_prompts': {'/tweet_prompts/report_interaction': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/tweet_prompts/show': {'limit': 180, 'remaining': 180, 'reset': 1542561591}}, 'moments': {'/moments/statuses/update': {'limit': 5, 'remaining': 5, 'reset': 1542561591}, '/moments/permissions': {'limit': 300, 'remaining': 300, 'reset': 1542561591}}, 'help': {'/help/tos': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/help/configuration': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/help/privacy': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/help/settings': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/help/languages': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'feedback': {'/feedback/show/:id': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/feedback/events': {'limit': 1000, 'remaining': 1000, 'reset': 1542561591}}, 'business_experience': {'/business_experience/dashboard_settings/destroy': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/business_experience/dashboard_features': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/business_experience/keywords': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/business_experience/dashboard_settings/update': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/business_experience/dashboard_settings/show': {'limit': 450, 'remaining': 450, 'reset': 1542561591}}, 'graphql&POST': {'/graphql&POST': {'limit': 2500, 'remaining': 2500, 'reset': 1542561591}}, 'friends': {'/friends/following/ids': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/friends/following/list': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/friends/list': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/friends/ids': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'sandbox': {'/sandbox/account_activity/webhooks/:id/subscriptions': {'limit': 500, 'remaining': 500, 'reset': 1542561591}}, 'drafts': {'/drafts/statuses/update': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/drafts/statuses/destroy': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/drafts/statuses/ids': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/drafts/statuses/list': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/drafts/statuses/show': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/drafts/statuses/create': {'limit': 450, 'remaining': 450, 'reset': 1542561591}}, 'direct_messages': {'/direct_messages/sent': {'limit': 300, 'remaining': 300, 'reset': 1542561591}, '/direct_messages/broadcasts/list': {'limit': 60, 'remaining': 60, 'reset': 1542561591}, '/direct_messages/subscribers/lists/members/show': {'limit': 1000, 'remaining': 1000, 'reset': 1542561591}, '/direct_messages/mark_read': {'limit': 1000, 'remaining': 1000, 'reset': 1542561591}, '/direct_messages/subscribers/ids': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/direct_messages/sent_and_received': {'limit': 300, 'remaining': 300, 'reset': 1542561591}, '/direct_messages/broadcasts/statuses/list': {'limit': 60, 'remaining': 60, 'reset': 1542561591}, '/direct_messages': {'limit': 300, 'remaining': 300, 'reset': 1542561591}, '/direct_messages/subscribers/lists/members/ids': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/direct_messages/subscribers/show': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/direct_messages/broadcasts/show': {'limit': 60, 'remaining': 60, 'reset': 1542561591}, '/direct_messages/broadcasts/statuses/show': {'limit': 60, 'remaining': 60, 'reset': 1542561591}, '/direct_messages/subscribers/lists/list': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/direct_messages/show': {'limit': 300, 'remaining': 300, 'reset': 1542561591}, '/direct_messages/events/list': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/direct_messages/subscribers/lists/show': {'limit': 180, 'remaining': 180, 'reset': 1542561591}, '/direct_messages/events/show': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'media': {'/media/upload': {'limit': 500, 'remaining': 500, 'reset': 1542561591}}, 'traffic': {'/traffic/map': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'account_activity': {'/account_activity/all/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/account_activity/all/:instance_name/subscriptions': {'limit': 500, 'remaining': 500, 'reset': 1542561591}, '/account_activity/direct_messages/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/account_activity/webhooks/:id/subscriptions/direct_messages/list': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/account_activity/webhooks/:id/subscriptions/all': {'limit': 500, 'remaining': 500, 'reset': 1542561591}, '/account_activity/direct_messages/:instance_name/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/account_activity/webhooks/:id/subscriptions/all/list': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/account_activity/webhooks/:id/subscriptions/direct_messages': {'limit': 500, 'remaining': 500, 'reset': 1542561591}, '/account_activity/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/account_activity/direct_messages/:instance_name/subscriptions': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/account_activity/webhooks/:id/subscriptions': {'limit': 500, 'remaining': 500, 'reset': 1542561591}, '/account_activity/all/:instance_name/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'account': {'/account/login_verification_enrollment': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/account/update_profile': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/account/verify_credentials': {'limit': 75, 'remaining': 75, 'reset': 1542561591}, '/account/settings': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'safety': {'/safety/detection_feedback': {'limit': 1000, 'remaining': 1000, 'reset': 1542561591}}, 'favorites': {'/favorites/list': {'limit': 75, 'remaining': 75, 'reset': 1542561591}}, 'device': {'/device/token': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'tweets': {'/tweets/stream/filter/rules': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/tweets/stream/filter/:instance_name': {'limit': 50, 'remaining': 50, 'reset': 1542561591}, '/tweets/search/:product/:label': {'limit': 1800, 'remaining': 1800, 'reset': 1542561591}, '/tweets/search/:product/:instance/counts': {'limit': 900, 'remaining': 900, 'reset': 1542561591}, '/tweets/stream/filter/rules/:instance_name/validation&POST': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/tweets/stream/filter/rules/:instance_name&POST': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/tweets/stream/filter/rules/:instance_name&DELETE': {'limit': 450, 'remaining': 450, 'reset': 1542561591}, '/tweets/stream/filter/rules/:instance_name/:rule_id': {'limit': 450, 'remaining': 450, 'reset': 1542561591}}, 'saved_searches': {'/saved_searches/destroy/:id': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/saved_searches/show/:id': {'limit': 15, 'remaining': 15, 'reset': 1542561591}, '/saved_searches/list': {'limit': 15, 'remaining': 15, 'reset': 1542561591}}, 'oauth': {'/oauth/invalidate_token': {'limit': 450, 'remaining': 450, 'reset': 1542561591}}, 'search': {'/search/tweets': {'limit': 180, 'remaining': 180, 'reset': 1542561591}}, 'trends': {'/trends/closest': {'limit': 75, 'remaining': 75, 'reset': 1542561591}, '/trends/available': {'limit': 75, 'remaining': 75, 'reset': 1542561591}, '/trends/place': {'limit': 75, 'remaining': 75, 'reset': 1542561591}}, 'live_pipeline': {'/live_pipeline/events': {'limit': 180, 'remaining': 180, 'reset': 1542561591}}}}













{'created_at': 'Tue Nov 13 20:39:34 +0000 2018', 'id': 1062444882969669637, 'id_str': '1062444882969669637', 'text': "someone: *venting about their problems and feelings to me*\n\nmy brain:\n\ndon't say it\ndon't say it\ndon't say it\ndon't… https://t.co/UBa5iNQiaN", 'truncated': True, 'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [], 'urls': [{'url': 'https://t.co/UBa5iNQiaN', 'expanded_url': 'https://twitter.com/i/web/status/1062444882969669637', 'display_url': 'twitter.com/i/web/status/1…', 'indices': [117, 140]}]}, 'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 377638035, 'id_str': '377638035', 'name': 'Osman 🥐', 'screen_name': 'mmatin2017', 'location': 'Charlotte, NC 📍', 'description': 'UNCC', 'url': 'https://t.co/4ICdKD23lj', 'entities': {'url': {'urls': [{'url': 'https://t.co/4ICdKD23lj', 'expanded_url': 'https://www.instagram.com/mmatin2017/', 'display_url': 'instagram.com/mmatin2017/', 'indices': [0, 23]}]}, 'description': {'urls': []}}, 'protected': False, 'followers_count': 164, 'friends_count': 143, 'listed_count': 0, 'created_at': 'Wed Sep 21 21:54:38 +0000 2011', 'favourites_count': 4148, 'utc_offset': None, 'time_zone': None, 'geo_enabled': True, 'verified': False, 'statuses_count': 1506, 'lang': 'en', 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': 'C0DEED', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1060401255061905408/oG9tNeHk_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1060401255061905408/oG9tNeHk_normal.jpg', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/377638035/1542150611', 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'has_extended_profile': True, 'default_profile': True, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 989, 'favorite_count': 3581, 'favorited': False, 'retweeted': False, 'lang': 'en'}, created_at=datetime.datetime(2018, 11, 13, 20, 39, 34), id=1062444882969669637, id_str='1062444882969669637', text="someone: *venting about their problems and feelings to me*\n\nmy brain:\n\ndon't say it\ndon't say it\ndon't say it\ndon't… https://t.co/UBa5iNQiaN", truncated=True, entities={'hashtags': [], 'symbols': [], 'user_mentions': [], 'urls': [{'url': 'https://t.co/UBa5iNQiaN', 'expanded_url': 'https://twitter.com/i/web/status/1062444882969669637', 'display_url': 'twitter.com/i/web/status/1…', 'indices': [117, 140]}]}, source='Twitter for iPhone', source_url='http://twitter.com/download/iphone', in_reply_to_status_id=None, in_reply_to_status_id_str=None, in_reply_to_user_id=None, in_reply_to_user_id_str=None, in_reply_to_screen_name=None, author=User(_api=<tweepy.api.API object at 0x0000024721DE86A0>, _json={'id': 377638035, 'id_str': '377638035', 'name': 'Osman 🥐', 'screen_name': 'mmatin2017', 'location': 'Charlotte, NC 📍', 'description': 'UNCC', 'url': 'https://t.co/4ICdKD23lj', 'entities': {'url': {'urls': [{'url': 'https://t.co/4ICdKD23lj', 'expanded_url': 'https://www.instagram.com/mmatin2017/', 'display_url': 'instagram.com/mmatin2017/', 'indices': [0, 23]}]}, 'description': {'urls': []}}, 'protected': False, 'followers_count': 164, 'friends_count': 143, 'listed_count': 0, 'created_at': 'Wed Sep 21 21:54:38 +0000 2011', 'favourites_count': 4148, 'utc_offset': None, 'time_zone': None, 'geo_enabled': True, 'verified': False, 'statuses_count': 1506, 'lang': 'en', 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': 'C0DEED', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1060401255061905408/oG9tNeHk_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1060401255061905408/oG9tNeHk_normal.jpg', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/377638035/1542150611', 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'has_extended_profile': True, 'default_profile': True, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, id=377638035, id_str='377638035', name='Osman 🥐', screen_name='mmatin2017', location='Charlotte, NC 📍', description='UNCC', url='https://t.co/4ICdKD23lj', entities={'url': {'urls': [{'url': 'https://t.co/4ICdKD23lj', 'expanded_url': 'https://www.instagram.com/mmatin2017/', 'display_url': 'instagram.com/mmatin2017/', 'indices': [0, 23]}]}, 'description': {'urls': []}}, protected=False, followers_count=164, friends_count=143, listed_count=0, created_at=datetime.datetime(2011, 9, 21, 21, 54, 38), favourites_count=4148, utc_offset=None, time_zone=None, geo_enabled=True, verified=False, statuses_count=1506, lang='en', contributors_enabled=False, is_translator=False, is_translation_enabled=False, profile_background_color='C0DEED', profile_background_image_url='http://abs.twimg.com/images/themes/theme1/bg.png', profile_background_image_url_https='https://abs.twimg.com/images/themes/theme1/bg.png', profile_background_tile=False, profile_image_url='http://pbs.twimg.com/profile_images/1060401255061905408/oG9tNeHk_normal.jpg', profile_image_url_https='https://pbs.twimg.com/profile_images/1060401255061905408/oG9tNeHk_normal.jpg', profile_banner_url='https://pbs.twimg.com/profile_banners/377638035/1542150611', profile_link_color='1DA1F2', profile_sidebar_border_color='C0DEED', profile_sidebar_fill_color='DDEEF6', profile_text_color='333333', profile_use_background_image=True, has_extended_profile=True, default_profile=True, default_profile_image=False, following=False, follow_request_sent=False, notifications=False, translator_type='none'), user=User(_api=<tweepy.api.API object at 0x0000024721DE86A0>, _json={'id': 377638035, 'id_str': '377638035', 'name': 'Osman 🥐', 'screen_name': 'mmatin2017', 'location': 'Charlotte, NC 📍', 'description': 'UNCC', 'url': 'https://t.co/4ICdKD23lj', 'entities': {'url': {'urls': [{'url': 'https://t.co/4ICdKD23lj', 'expanded_url': 'https://www.instagram.com/mmatin2017/', 'display_url': 'instagram.com/mmatin2017/', 'indices': [0, 23]}]}, 'description': {'urls': []}}, 'protected': False, 'followers_count': 164, 'friends_count': 143, 'listed_count': 0, 'created_at': 'Wed Sep 21 21:54:38 +0000 2011', 'favourites_count': 4148, 'utc_offset': None, 'time_zone': None, 'geo_enabled': True, 'verified': False, 'statuses_count': 1506, 'lang': 'en', 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': 'C0DEED', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1060401255061905408/oG9tNeHk_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1060401255061905408/oG9tNeHk_normal.jpg', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/377638035/1542150611', 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'has_extended_profile': True, 'default_profile': True, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, id=377638035, id_str='377638035', name='Osman 🥐', screen_name='mmatin2017', location='Charlotte, NC 📍', description='UNCC', url='https://t.co/4ICdKD23lj', entities={'url': {'urls': [{'url': 'https://t.co/4ICdKD23lj', 'expanded_url': 'https://www.instagram.com/mmatin2017/', 'display_url': 'instagram.com/mmatin2017/', 'indices': [0, 23]}]}, 'description': {'urls': []}}, protected=False, followers_count=164, friends_count=143, listed_count=0, created_at=datetime.datetime(2011, 9, 21, 21, 54, 38), favourites_count=4148, utc_offset=None, time_zone=None, geo_enabled=True, verified=False, statuses_count=1506, lang='en', contributors_enabled=False, is_translator=False, is_translation_enabled=False, profile_background_color='C0DEED', profile_background_image_url='http://abs.twimg.com/images/themes/theme1/bg.png', profile_background_image_url_https='https://abs.twimg.com/images/themes/theme1/bg.png', profile_background_tile=False, profile_image_url='http://pbs.twimg.com/profile_images/1060401255061905408/oG9tNeHk_normal.jpg', profile_image_url_https='https://pbs.twimg.com/profile_images/1060401255061905408/oG9tNeHk_normal.jpg', profile_banner_url='https://pbs.twimg.com/profile_banners/377638035/1542150611', profile_link_color='1DA1F2', profile_sidebar_border_color='C0DEED', profile_sidebar_fill_color='DDEEF6', profile_text_color='333333', profile_use_background_image=True, has_extended_profile=True, default_profile=True, default_profile_image=False, following=False, follow_request_sent=False, notifications=False, translator_type='none'), geo=None, coordinates=None, place=None, contributors=None, is_quote_status=False, retweet_count=989, favorite_count=3581, favorited=False, retweeted=False, lang='en')


























(base) C:\Users\Julian\Documents\GitHub>py3
'py3' is not recognized as an internal or external command,
operable program or batch file.

(base) C:\Users\Julian\Documents\GitHub>activate py3

(py3) C:\Users\Julian\Documents\GitHub>python
Python 3.7.1 (default, Oct 28 2018, 08:39:03) [MSC v.1912 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import tweepy #http://docs.tweepy.org/en/v3.6.0/
>>>
>>>
>>> import networkx as nx
>>>
>>>
>>> import json
>>> import time
>>> import asyncio
>>>
>>>
>>> access_token= "1043132884759072769-aqQYY7XQ2Rlj5CdXdLRgv0I3us3Dxs"
>>> access_token_secret = "hIdttcfhoLqvoNVVvs7myVocBlVoKisqGgonqrk6WFXAh"
>>> consumer_key= "YAUrjz6OEkKtVsnNuG0ZfdI7t"
>>> consumer_secret= "vs6i2CdSphMn9MXoNg2azdSMqL0fzjQxIpLYXud3CajqFj8xZw"
>>>
>>>
>>> #authetication requests
... auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
>>> auth.set_access_token(access_token, access_token_secret)
>>>
>>>
>>> #create api variable
... api = tweepy.API(auth)
>>>
>>> rate_status = api.rate_limit_status() #GET /application/rate_limit_status
>>>     empty, parent_string, child = api_string.split("/", 2)
  File "<stdin>", line 1
    empty, parent_string, child = api_string.split("/", 2)
    ^
IndentationError: unexpected indent
>>>     reset_time = rate_status['resources'][parent_string][api_string]['reset']
  File "<stdin>", line 1
    reset_time = rate_status['resources'][parent_string][api_string]['reset']
    ^
IndentationError: unexpected indent
>>> rate_status = api.rate_limit_status() #GET /application/rate_limit_status
>>> api_string = '/followers/list'
>>>     empty, parent_string, child = api_string.split("/", 2)
  File "<stdin>", line 1
    empty, parent_string, child = api_string.split("/", 2)
    ^
IndentationError: unexpected indent
>>> empty, parent_string, child = api_string.split("/", 2)
>>> empty
''
>>> parent_string
'followers'
>>> child
'list'
>>> api_string
'/followers/list'
>>> reset_time = rate_status['resources'][parent_string][api_string]['reset']
>>> time_left = reset_time - int(time.time())
>>> time_left
790
>>> rate_status = api.rate_limit_status()
>>> reset_time = rate_status['resources'][parent_string][api_string]['reset']
>>> reset_time
1542598756
>>> time_left = reset_time - int(time.time())
>>> time_left
879
>>> rate_status
{'rate_limit_context': {'access_token': '1043132884759072769-aqQYY7XQ2Rlj5CdXdLRgv0I3us3Dxs'}, 'resources': {'lists': {'/lists/list': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/lists/memberships': {'limit': 75, 'remaining': 75, 'reset': 1542598756}, '/lists/subscribers/show': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/lists/members': {'limit': 900, 'remaining': 900, 'reset': 1542598756}, '/lists/subscriptions': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/lists/show': {'limit': 75, 'remaining': 75, 'reset': 1542598756}, '/lists/ownerships': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/lists/subscribers': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/lists/members/show': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/lists/statuses': {'limit': 900, 'remaining': 900, 'reset': 1542598756}}, 'application': {'/application/rate_limit_status': {'limit': 180, 'remaining': 173, 'reset': 1542598358}}, 'mutes': {'/mutes/users/list': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/mutes/users/ids': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'live_video_stream': {'/live_video_stream/status/:id': {'limit': 1000, 'remaining': 1000, 'reset': 1542598756}}, 'friendships': {'/friendships/outgoing': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/friendships/list': {'limit': 200, 'remaining': 200, 'reset': 1542598756}, '/friendships/no_retweets/ids': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/friendships/lookup': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/friendships/incoming': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/friendships/show': {'limit': 180, 'remaining': 180, 'reset': 1542598756}}, 'guide': {'/guide': {'limit': 180, 'remaining': 180, 'reset': 1542598756}}, 'auth': {'/auth/csrf_token': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'blocks': {'/blocks/list': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/blocks/ids': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'geo': {'/geo/similar_places': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/geo/id/:place_id': {'limit': 75, 'remaining': 75, 'reset': 1542598756}, '/geo/reverse_geocode': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/geo/search': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'users': {'/users/report_spam': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/users/contributors/pending': {'limit': 2000, 'remaining': 2000, 'reset': 1542598756}, '/users/show/:id': {'limit': 900, 'remaining': 900, 'reset': 1542598756}, '/users/search': {'limit': 900, 'remaining': 900, 'reset': 1542598756}, '/users/suggestions/:slug': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/users/contributees/pending': {'limit': 200, 'remaining': 200, 'reset': 1542598756}, '/users/derived_info': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/users/profile_banner': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/users/suggestions/:slug/members': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/users/lookup': {'limit': 900, 'remaining': 900, 'reset': 1542598756}, '/users/suggestions': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'followers': {'/followers/ids': {'limit': 15, 'remaining': 0, 'reset': 1542598354}, '/followers/list': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'collections': {'/collections/list': {'limit': 1000, 'remaining': 1000, 'reset': 1542598756}, '/collections/entries': {'limit': 1000, 'remaining': 1000, 'reset': 1542598756}, '/collections/show': {'limit': 1000, 'remaining': 1000, 'reset': 1542598756}}, 'statuses': {'/statuses/retweeters/ids': {'limit': 75, 'remaining': 75, 'reset': 1542598756}, '/statuses/retweets_of_me': {'limit': 75, 'remaining': 75, 'reset': 1542598756}, '/statuses/home_timeline': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/statuses/show/:id': {'limit': 900, 'remaining': 900, 'reset': 1542598756}, '/statuses/user_timeline': {'limit': 900, 'remaining': 900, 'reset': 1542598756}, '/statuses/friends': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/statuses/retweets/:id': {'limit': 75, 'remaining': 68, 'reset': 1542598024}, '/statuses/mentions_timeline': {'limit': 75, 'remaining': 75, 'reset': 1542598756}, '/statuses/oembed': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/statuses/lookup': {'limit': 900, 'remaining': 900, 'reset': 1542598756}}, 'custom_profiles': {'/custom_profiles/list': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/custom_profiles/show': {'limit': 180, 'remaining': 180, 'reset': 1542598756}}, 'webhooks': {'/webhooks/subscriptions/direct_messages': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'contacts': {'/contacts/uploaded_by': {'limit': 300, 'remaining': 300, 'reset': 1542598756}, '/contacts/users': {'limit': 300, 'remaining': 300, 'reset': 1542598756}, '/contacts/addressbook': {'limit': 300, 'remaining': 300, 'reset': 1542598756}, '/contacts/users_and_uploaded_by': {'limit': 300, 'remaining': 300, 'reset': 1542598756}, '/contacts/delete/status': {'limit': 300, 'remaining': 300, 'reset': 1542598756}}, 'i': {'/i/config': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'tweet_prompts': {'/tweet_prompts/report_interaction': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/tweet_prompts/show': {'limit': 180, 'remaining': 180, 'reset': 1542598756}}, 'moments': {'/moments/statuses/update': {'limit': 5, 'remaining': 5, 'reset': 1542598756}, '/moments/permissions': {'limit': 300, 'remaining': 300, 'reset': 1542598756}}, 'help': {'/help/tos': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/help/configuration': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/help/privacy': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/help/settings': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/help/languages': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'feedback': {'/feedback/show/:id': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/feedback/events': {'limit': 1000, 'remaining': 1000, 'reset': 1542598756}}, 'business_experience': {'/business_experience/dashboard_settings/destroy': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/business_experience/dashboard_features': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/business_experience/keywords': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/business_experience/dashboard_settings/update': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/business_experience/dashboard_settings/show': {'limit': 450, 'remaining': 450, 'reset': 1542598756}}, 'graphql&POST': {'/graphql&POST': {'limit': 2500, 'remaining': 2500, 'reset': 1542598756}}, 'friends': {'/friends/following/ids': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/friends/following/list': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/friends/list': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/friends/ids': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'sandbox': {'/sandbox/account_activity/webhooks/:id/subscriptions': {'limit': 500, 'remaining': 500, 'reset': 1542598756}}, 'drafts': {'/drafts/statuses/update': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/drafts/statuses/destroy': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/drafts/statuses/ids': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/drafts/statuses/list': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/drafts/statuses/show': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/drafts/statuses/create': {'limit': 450, 'remaining': 450, 'reset': 1542598756}}, 'direct_messages': {'/direct_messages/sent': {'limit': 300, 'remaining': 300, 'reset': 1542598756}, '/direct_messages/broadcasts/list': {'limit': 60, 'remaining': 60, 'reset': 1542598756}, '/direct_messages/subscribers/lists/members/show': {'limit': 1000, 'remaining': 1000, 'reset': 1542598756}, '/direct_messages/mark_read': {'limit': 1000, 'remaining': 1000, 'reset': 1542598756}, '/direct_messages/subscribers/ids': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/direct_messages/sent_and_received': {'limit': 300, 'remaining': 300, 'reset': 1542598756}, '/direct_messages/broadcasts/statuses/list': {'limit': 60, 'remaining': 60, 'reset': 1542598756}, '/direct_messages': {'limit': 300, 'remaining': 300, 'reset': 1542598756}, '/direct_messages/subscribers/lists/members/ids': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/direct_messages/subscribers/show': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/direct_messages/broadcasts/show': {'limit': 60, 'remaining': 60, 'reset': 1542598756}, '/direct_messages/broadcasts/statuses/show': {'limit': 60, 'remaining': 60, 'reset': 1542598756}, '/direct_messages/subscribers/lists/list': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/direct_messages/show': {'limit': 300, 'remaining': 300, 'reset': 1542598756}, '/direct_messages/events/list': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/direct_messages/subscribers/lists/show': {'limit': 180, 'remaining': 180, 'reset': 1542598756}, '/direct_messages/events/show': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'media': {'/media/upload': {'limit': 500, 'remaining': 500, 'reset': 1542598756}}, 'traffic': {'/traffic/map': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'account_activity': {'/account_activity/all/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/account_activity/all/:instance_name/subscriptions': {'limit': 500, 'remaining': 500, 'reset': 1542598756}, '/account_activity/direct_messages/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/account_activity/webhooks/:id/subscriptions/direct_messages/list': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/account_activity/webhooks/:id/subscriptions/all': {'limit': 500, 'remaining': 500, 'reset': 1542598756}, '/account_activity/direct_messages/:instance_name/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/account_activity/webhooks/:id/subscriptions/all/list': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/account_activity/webhooks/:id/subscriptions/direct_messages': {'limit': 500, 'remaining': 500, 'reset': 1542598756}, '/account_activity/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/account_activity/direct_messages/:instance_name/subscriptions': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/account_activity/webhooks/:id/subscriptions': {'limit': 500, 'remaining': 500, 'reset': 1542598756}, '/account_activity/all/:instance_name/webhooks': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'account': {'/account/login_verification_enrollment': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/account/update_profile': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/account/verify_credentials': {'limit': 75, 'remaining': 75, 'reset': 1542598756}, '/account/settings': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'safety': {'/safety/detection_feedback': {'limit': 1000, 'remaining': 1000, 'reset': 1542598756}}, 'favorites': {'/favorites/list': {'limit': 75, 'remaining': 75, 'reset': 1542598756}}, 'device': {'/device/token': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'tweets': {'/tweets/stream/filter/rules': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/tweets/stream/filter/:instance_name': {'limit': 50, 'remaining': 50, 'reset': 1542598756}, '/tweets/search/:product/:label': {'limit': 1800, 'remaining': 1800, 'reset': 1542598756}, '/tweets/search/:product/:instance/counts': {'limit': 900, 'remaining': 900, 'reset': 1542598756}, '/tweets/stream/filter/rules/:instance_name/validation&POST': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/tweets/stream/filter/rules/:instance_name&POST': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/tweets/stream/filter/rules/:instance_name&DELETE': {'limit': 450, 'remaining': 450, 'reset': 1542598756}, '/tweets/stream/filter/rules/:instance_name/:rule_id': {'limit': 450, 'remaining': 450, 'reset': 1542598756}}, 'saved_searches': {'/saved_searches/destroy/:id': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/saved_searches/show/:id': {'limit': 15, 'remaining': 15, 'reset': 1542598756}, '/saved_searches/list': {'limit': 15, 'remaining': 15, 'reset': 1542598756}}, 'oauth': {'/oauth/invalidate_token': {'limit': 450, 'remaining': 450, 'reset': 1542598756}}, 'search': {'/search/tweets': {'limit': 180, 'remaining': 180, 'reset': 1542598756}}, 'trends': {'/trends/closest': {'limit': 75, 'remaining': 75, 'reset': 1542598756}, '/trends/available': {'limit': 75, 'remaining': 75, 'reset': 1542598756}, '/trends/place': {'limit': 75, 'remaining': 75, 'reset': 1542598756}}, 'live_pipeline': {'/live_pipeline/events': {'limit': 180, 'remaining': 180, 'reset': 1542598756}}}}
