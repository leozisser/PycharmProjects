import requests, operator, time


token = '58e7a379bea01a3c940baa413e9e8a78e3393570bb17eff33b267b82759124b5c333afd2df2022b28737d'


def get_friends(usr_id):

    targetid = usr_id

    userid = targetid
    print('userid', userid)

    friends_apilink = 'https://api.vk.com/method/friends.get'

    fields = {'user_id': userid, 'order':'random'}  # WHY IS IT DOING WHAT IT IS DOING?

    params_ = {'access_token': token, 'user_id': userid, 'order':'random'}  #, 'fields': fields}
    # print('params', params_)
    crawler = requests.get(friends_apilink, params=params_)
    time.sleep(0.2)

    batch = crawler.json()
    print('batch',batch)
    id_list = batch['response']
    return id_list

friends_of_friends = {}

primary_id = '428604605'
primary_id_list = get_friends(primary_id)

for friend1 in primary_id_list[:20]:
    secondary_id_list = get_friends(friend1)
    for friend2 in secondary_id_list:
        if friend2 not in friends_of_friends and str(friend2) != primary_id:
            friends_of_friends[friend2] = 0
        elif friend2 in friends_of_friends:
            friends_of_friends[friend2] +=1

friends_of_friends = { k:v for k, v in friends_of_friends.items() if v > 1 }

print('unsorted', friends_of_friends)
targets_sorted = sorted(friends_of_friends.items(), key=operator.itemgetter(1), reverse=True)

print('sorted', targets_sorted)

"""
 use this method https://vk.com/dev/execute to raise request limit 25 times
"""





