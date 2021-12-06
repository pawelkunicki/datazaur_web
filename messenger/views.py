import datetime
from itertools import chain

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .models import Message
from .forms import SendMessage, FindUsers
from website.models import UserProfile
# Create your views here.


@login_required
def messenger(request):
    context = {}
    profile = UserProfile.objects.get(user=request.user)
    friends = profile.friends.all()

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
    else:

        print('useradd')
        print(request.POST)
        friend = UserProfile.objects.get(user=User.objects.get(id=request.POST['add_friend']))
        if profile.friends.filter(user=friend.user).exists():
            print('friends already')
        else:
            profile.friends.add(friend)
            print('saved friends')

        return render(request, 'messenger/messenger.html', context)

    return render(request, 'messenger/messenger.html', context)


def get_messages(request, friend_id):
    user = UserProfile.objects.get(user=request.user)
    recipient = UserProfile.objects.get(id=friend_id)
    sent_msgs = Message.objects.filter(sender=user, recipient=recipient).values()
    received_msgs = Message.objects.filter(sender=recipient, recipient=user).values()
    msgs = sorted(
        chain(sent_msgs, received_msgs),
        key=lambda instance: instance['timestamp'])

    for msg in msgs:
        msg['sender_id'] = UserProfile.objects.get(id=msg['sender_id']).user.username

    print(msgs)
    print(type(msgs))
    return JsonResponse({'messages': msgs})

@login_required
def chat(request, friend_id):

    context = {}
    user = UserProfile.objects.get(user=request.user)
    friends = user.friends.all()
    recipient = UserProfile.objects.get(id=friend_id)

    print(friends)
    context['profile'] = user
    context['friends'] = friends
    context['recipient'] = recipient
    context['find_users'] = FindUsers()
    context['send_message'] = SendMessage()
    context['search_results'] = []

    sent_msgs = Message.objects.filter(sender=user, recipient=recipient)
    received_msgs = Message.objects.filter(sender=recipient, recipient=user)
    msgs = sorted(
        chain(sent_msgs, received_msgs),
        key=lambda instance: instance.timestamp)

    context['messages'] = msgs


    if request.method == 'POST':
        print('msg')
        print(request.user)
        print(request.POST)
        message = request.POST['message_text']
        msg = Message.objects.create(sender=user, recipient=recipient, content=message, timestamp=datetime.datetime.now().timestamp())
        return HttpResponseRedirect(reverse('messenger:chat', args=(friend_id,)))

    return render(request, 'messenger/chat.html', context)





class MessengerView(TemplateView):
    template_name = 'messenger/messenger.html'
    #find_form

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return render(request, self.template_name, context)

    @login_required
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)


        return HttpResponseRedirect(reverse('messenger:messenger'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter()



