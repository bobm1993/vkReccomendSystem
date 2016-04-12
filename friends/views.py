from django.shortcuts import render
import vk
import vk.exceptions
import time
import socket
import errno
import operator

host = '127.0.0.1'
port = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def home(request):
    current_id = request.POST.get('current_id')
    return render(request, 'friends/home.html', {'current_id': current_id})


def friends_list(request):
    current_id = request.POST.get('your_id')
    friends = friends_get(current_id)
    full_super_friend_list = []
    rates = []
    recommends_top10 = []
    for friend in friends:
        time.sleep(0.1)
        fr_friends = friends_get(friend)
        print(fr_friends)
        for fr in fr_friends:
            if fr not in friends and fr != int(current_id):
                full_super_friend_list.append(fr)

    super_friend_list = set(full_super_friend_list)

    k = len(full_super_friend_list)
    for sup in super_friend_list:
        i = full_super_friend_list.count(sup) / k
        print(i)
        rates.append(i)

    # recommends = users_get(super_friend_list)
    diction = dict(zip(super_friend_list, rates))
    diction_sort = sorted(diction.items(), key=operator.itemgetter(1), reverse=True)
    diction_top10 = diction_sort[:10]

    for row in diction_top10:
        recommends_top10.append(row[0])

    return render(request, 'friends/recommend_list.html', {'rec_list': recommends_top10})


def friends_get(ide):
    session = \
        vk.Session(access_token='be2ed15f660f93722c8be1255d7e65a47c2350a220231aa90514029c0c2b2ff071548c66ed56edd275fd2')
    vkapi = vk.API(session)
    friends_me = []
    try:
        friends_me = vkapi.friends.get(user_id=ide)
    except vk.exceptions.VkException:
        pass
    except socket.error as error:
        if error.errno == errno.WSAECONNRESET:
            connect()
        else:
            raise
    return friends_me


# def users_get(profiles):
#     session = \
#         vk.Session(access_token='be2ed15f660f93722c8be1255d7e65a47c2350a220231aa90514029c0c2b2ff071548c66ed56edd275fd2')
#     vkapi = vk.API(session)
#     names = []
#     for profile in profiles:
#         try:
#             x = vkapi.users.get(user_id=profile)
#             names.append(x[0])
#             print(x)
#         except KeyError:
#             pass
#         time.sleep(0.34)
#     return names


def loop():
    try:
        while 1:
            print(s.recv(512))
    except socket.error:
        s.close()
        connect()


def connect():
    s.connect((host, port))
    loop()