import datetime

from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import SendMessage, FindUsers
from website.models import UserProfile, FriendLists
# Create your views here.


@login_required
def messenger(request):
    context = {}
    profile = UserProfile.objects.get(user=request.user)
    if FriendLists.objects.filter(user=profile).exists():
        friends = FriendLists.objects.filter(user=profile)
    else:
        friends = []

    print(friends)
    context['profile'] = profile
    context['friends'] = friends
    context['recipient'] = None
    context['find_users'] = FindUsers()
    context['send_message'] = SendMessage()
    context['search_results'] = []

    if request.method == 'GET':
        print('get')
        print(request.GET)

        if 'find_users' in str(request.GET):
            print('find')
            find_form = FindUsers(request.GET)
            if find_form.is_valid():
                form_data = find_form.cleaned_data
                name = form_data['name']
                context['search_results'] = User.objects.filter(username__icontains=name)
                print(context['search_results'])
            else:
                print(f'error {find_form.errors}')

        elif 'new_msg' in str(request.GET):
            print('new_msg')
            print(request.GET)
            recipient = UserProfile.objects.get(id=request.GET['new_msg'])
            context['recipient'] = recipient
            print('got msgs')
            context['messages'] = Message.objects.filter(sender=profile, recipient=recipient)


    elif request.method == 'POST':
        if 'message_text' in str(request.POST):
            print('msg')
            print(request.user)
            print(request.POST)
            message = request.POST['message_text']
            sender = UserProfile.objects.get(user=request.user)
            recipient = UserProfile.objects.get(id=request.POST['recipient_id'])
            Message.objects.create(sender=sender, recipient=recipient, content=message, timestamp=datetime.datetime.now().timestamp()).save()
            context['recipient'] = recipient
            context['messages'] = Message.objects.filter(sender=profile, recipient=recipient)
            return render(request, 'messenger/messenger.html', context)

        elif 'add_friend' in str(request.POST):
            print('useradd')
            print(request.POST)
            target_user = UserProfile.objects.get(user=User.objects.get(id=request.POST['add_friend']))
            if FriendLists.objects.filter(user=profile, friend=target_user).exists():
                print('friends already')
            else:
                friends = FriendLists.objects.create(user=profile, friend=target_user)
                friends.save()
                print('saved friends')

            return render(request, 'messenger/messenger.html', context)

        elif 'follow' in str(request.POST):
            pass

    return render(request, 'messenger/messenger.html', context)



def top_traders(request):
    context = {}

    return render(request, 'social/top_traders.html', context)


