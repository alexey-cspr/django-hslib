from abc import ABC

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import View
from . import email

from decks.forms import SignUpForm, SendEmailForm, PostDeck
from decks.models import Deck
from decks.tokens import account_activation_token


class DeckView(View):
    def get(self, request):
        decks = Deck.objects.all()
        return render(request, "decks/main_page.html", {"deck_list": decks})


class DecksView(View):
    def get(self, request, slug):
        decks = Deck.objects.filter(name=slug)
        return render(request, "decks/decks_list.html", {"decks": decks})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email.send_email(user.email, subject, message)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activation_email_sent(request):
    return render(request, 'registration/activation_email_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'registration/account_activation_invalid.html')


class SendEmailView(UserPassesTestMixin, View):
    login_url = '/accounts/login'

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request):
        form = SendEmailForm(request.POST)

        if form.is_valid():
            users = form.cleaned_data['users']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            for user in users:
                email.send_email(user.email, subject, message)

            messages.info(request, 'Emails successfully sent.')

            return redirect('/')

        return redirect('/')


def new_deck(request):
    template = "decks/new_deck.html"
    form = PostDeck()
    if request.method == 'POST':
        form = PostDeck(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, template, context)


def update_deck(request, pk):
    decks = Deck.objects.get(id=pk)
    form = PostDeck(instance=decks)
    if request.method == 'POST':
        form = PostDeck(request.POST, request.FILES, instance=decks)
        if form.is_valid():
            form.save()
            return redirect('/')
    template = "decks/update_deck.html"
    context = {'form': form}
    return render(request, template, context)


def delete_deck(request, pk):
    decks = Deck.objects.get(id=pk)
    context = {'item': decks}
    template = "decks/delete_deck.html"
    if request.method == 'POST':
        decks.delete()
        return redirect('/')
    return render(request, template, context)

# required_https_methods()
# login_required()
# grip_page()
