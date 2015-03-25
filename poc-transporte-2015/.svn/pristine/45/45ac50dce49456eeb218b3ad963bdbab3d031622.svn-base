# -*- coding: utf-8 -*-
import sys
import twitter
from MakeTwitterRequest import make_twitter_request
import functools

#SCREEN_NAME = sys.argv[1]
#MAX_IDS = int(sys.argv[2])

SCREEN_NAME = "lglima"
MAX_IDS = 200

class GetFriendsFollowersInfo:
    
    def __init__(self, t):
        
        self.t = t
        
#         get_friends_ids = functools.partial(make_twitter_request, t, t.friends.ids)
#     
#         # XXX: Ditto if you want to do the same thing to get followers...
#     
#         get_followers_ids = functools.partial(make_twitter_request, t, t.followers.ids)
#     
#         cursor = -1
#         ids = []
#         while cursor != 0:
#     
#             # Use make_twitter_request via the partially bound callable...
#     
#             #response = get_friends_ids(screen_name=SCREEN_NAME, cursor=cursor)
#             response = get_followers_ids(screen_name=SCREEN_NAME, cursor=cursor)
#             ids += response['ids']
#             cursor = response['next_cursor']
#     
#             print >> sys.stderr, 'Fetched %i total ids for %s' % (len(ids), SCREEN_NAME)
#     
#             # Consider storing the ids to disk during each iteration to provide an
#             # an additional layer of protection from exceptional circumstances
#     
#             if len(ids) >= MAX_IDS:
#                 break
#     
#         # Pegando as informações dos usuários e mostrando na tela
#         userIds = get_info_by_id(t, ids)
#         print userIds
    
    def get_info_by_id(self, ids):
    
        id_to_info = {}
    
        while len(ids) > 0:
    
            # Processando 100 ids de cada vez...
            ids_str = ','.join([str(_id) for _id in ids[:100]])
            ids = ids[100:]
            response = make_twitter_request(self.t,
                                          getattr(getattr(self.t, "users"), "lookup"),
                                          user_id=ids_str, _method='GET')
            if response is None:
                break
            if type(response) is dict:  # Handle Twitter API quirk
                response = [response]
            for user_info in response:
                id_to_info[user_info['id']] = user_info
        return id_to_info
    
    def get_info_by_screen_name(self, screen_names):
    
        sn_to_info = {}
    
        while len(screen_names) > 0:
    
            # Process 100 ids at a time...
    
            screen_names_str = ','.join([str(sn) for sn in screen_names[:100]])
            screen_names = screen_names[100:]
    
            response = make_twitter_request(self.t,
                                          getattr(getattr(self.t, "users"), "lookup"),
                                          screen_name=screen_names_str)
    
            if response is None:
                break
    
            if type(response) is dict:  # Handle Twitter API quirk
                response = [response]
    
            for user_info in response:
                sn_to_info[user_info['screen_name']] = user_info
    
        return sn_to_info
    
        