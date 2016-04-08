from django.shortcuts import render
import vk
import time


def home(request):
    current_id = request.POST.get('current_id')
    return render(request, 'friends/home.html', {'current_id': current_id})


def friends_list(request):
    session = \
        vk.Session(access_token='be2ed15f660f93722c8be1255d7e65a47c2350a220231aa90514029c0c2b2ff071548c66ed56edd275fd2')
    vkapi = vk.API(session)
    current_id = request.POST.get('current_id')
    friends = vkapi.friends.get(user_id=current_id)
    last_names = []
    for friend in friends:
        x = vkapi.users.get(user_id=friend)
        last_names.append(x[0]['last_name'])
        time.sleep(0.34)
    return render(request, 'friends/friends_list.html', {'last_names': last_names})
