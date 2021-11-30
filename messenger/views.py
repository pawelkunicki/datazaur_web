import datetime

from django.shortcuts import render, HttpResponseRedirect
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

        elif 'add_friend' in str(request.POST):
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



@login_required
def chat(request, user_id):

    context = {}
    profile = UserProfile.objects.get(user=request.user)
    friends = profile.friends.all()
    recipient = UserProfile.objects.get(id=user_id)

    print(friends)
    context['profile'] = profile
    context['friends'] = friends
    context['recipient'] = recipient
    context['find_users'] = FindUsers()
    context['send_message'] = SendMessage()
    context['search_results'] = []

    context['messages'] = Message.objects.filter(sender=request.user, recipient=recipient.user)


    if request.method == 'POST':

        print('msg')
        print(request.user)
        print(request.POST)
        message = request.POST['message_text']
        sender = UserProfile.objects.get(user=request.user)
        #recipient = UserProfile.objects.get(id=request.POST['recipient_id'])
        recipient = UserProfile.objects.get(id=user_id)

        msg = Message.objects.create(sender=sender.user, recipient=recipient.user, content=message, timestamp=datetime.datetime.now().timestamp())
        msg.save()
        context['recipient'] = recipient
        context['messages'] = Message.objects.filter(sender=profile, recipient=recipient)



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



