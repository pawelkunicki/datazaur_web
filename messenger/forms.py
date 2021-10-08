from django import forms
from website.models import UserProfile


class SendMessage(forms.Form):
    recipient = forms.ChoiceField(label='Recipient', choices=())
    message = forms.Textarea()




class FindUsers(forms.Form):
    name = forms.CharField(label='Username/email', max_length=32)


class AddFriend(forms.Form):
    user = forms.HiddenInput()
