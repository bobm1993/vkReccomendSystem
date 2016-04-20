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
    current_user = user_get(current_id)
    if 'city' in current_user:
        current_user_city = current_user['city']
    else:
        current_user_city = 0
    if 'home_town' in current_user:
        current_user_home_town = current_user['home_town']
    else:
        current_user_home_town = ''
    current_user_univ = []
    if 'universities' in current_user:
        for university in current_user['universities']:
            current_user_univ.append(university.get('id'))
    current_user_schools = []
    if 'schools' in current_user:
        for school in current_user['schools']:
            current_user_schools.append(school.get('id'))
    if 'personal' in current_user:
        personal = current_user['personal']
        if 'alcohol' in personal:
            current_user_alcohol = personal.get('alcohol')
        else:
            current_user_alcohol = 0
        if 'political' in personal:
            current_user_political = personal.get('political')
        else:
            current_user_political = 0
        if 'smoking' in personal:
            current_user_smoking = personal.get('smoking')
        else:
            current_user_smoking = 0
    else:
        current_user_alcohol = 0
        current_user_political = 0
        current_user_smoking = 0

    friends = friends_get(current_id)
    followers = followers_get(current_id)['items']
    subscriptions = subscriptions_get(current_id)['users']['items']
    full_super_friend_list = []
    rates = []
    for friend in friends:
        time.sleep(0.1)
        fr_friends = friends_get(friend)
        print(fr_friends)
        for fr in fr_friends:
            if fr not in friends and fr != int(current_id) and fr not in subscriptions and fr not in followers:
                full_super_friend_list.append(fr)

    super_friend_list = set(full_super_friend_list)

    k = len(full_super_friend_list)
    for sup in super_friend_list:
        i = full_super_friend_list.count(sup) / k
        print(i)
        rates.append(i)

    diction = dict(zip(super_friend_list, rates))
    diction_sort = sorted(diction.items(), key=operator.itemgetter(1), reverse=True)
    diction_top10 = diction_sort[:10]

    profiles = []
    ratings = []
    for row in diction_top10:
        profiles.append(user_get(row[0]))
        ratings.append(row[1])

    i = 0
    for row in profiles:
        if 'city' in row and row['city'] == current_user_city:
            ratings[i] *= 1.25
        if 'home_town' in row and row['home_town'] == current_user_home_town:
            ratings[i] *= 1.25
        if 'universities' in row:
            for university in row['universities']:
                if university.get('id') in current_user_univ:
                    ratings[i] *= 1.25
        if 'schools' in row:
            for school in row['schools']:
                if school.get('id') in current_user_schools:
                    ratings[i] *= 1.25
        if 'personal' in row:
            personal = row['personal']
            if 'alcohol' in personal and personal.get('alcohol') == current_user_alcohol:
                ratings[i] *= 1.25
            if 'political' in personal and personal.get('political') == current_user_political:
                ratings[i] *= 1.25
            if 'smoking' in personal and personal.get('smoking') == current_user_smoking:
                ratings[i] *= 1.25
        i += 1

    recommends = list(zip(profiles, ratings))
    recommends_sort = sorted(recommends, key=operator.itemgetter(1), reverse=True)
    recommend_list = []
    for row in recommends_sort:
        recommend_list.append(row[0])

    return render(request, 'friends/recommend_list.html', {'rec_list': recommend_list})


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


def user_get(profile):
    session = \
        vk.Session(access_token='be2ed15f660f93722c8be1255d7e65a47c2350a220231aa90514029c0c2b2ff071548c66ed56edd275fd2')
    vkapi = vk.API(session)
    try:
        x = vkapi.users.get(user_id=profile, fields=['city', 'home_town', 'photo_50', 'universities', 'schools',
                                                     'personal'])
        name = x[0]
        print(x)
    except KeyError:
        pass
    time.sleep(0.34)
    return name


def subscriptions_get(ide):
    session = \
        vk.Session(access_token='be2ed15f660f93722c8be1255d7e65a47c2350a220231aa90514029c0c2b2ff071548c66ed56edd275fd2')
    vkapi = vk.API(session)
    try:
        x = vkapi.users.getSubscriptions(user_id=ide)
    except KeyError:
        pass
    time.sleep(0.34)
    return x


def followers_get(ide):
    session = \
        vk.Session(access_token='be2ed15f660f93722c8be1255d7e65a47c2350a220231aa90514029c0c2b2ff071548c66ed56edd275fd2')
    vkapi = vk.API(session)
    try:
        x = vkapi.users.getFollowers(user_id=ide)
    except KeyError:
        pass
    time.sleep(0.34)
    return x


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