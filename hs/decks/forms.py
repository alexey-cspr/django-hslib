from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from decks.models import Deck


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SendEmailForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea)
    users = forms.ModelMultipleChoiceField(label="To", queryset=User.objects.all(), widget=forms.SelectMultiple())


class PostDeck(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'deck_tier', 'archetype', 'url', 'player', 'image', 'review']
