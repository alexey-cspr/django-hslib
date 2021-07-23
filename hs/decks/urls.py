from django.conf.urls import url
from django.urls import path

from . import views
from .views import activate, activation_email_sent, new_deck, SendEmailView, update_deck, delete_deck

urlpatterns = [
    path("", views.DeckView.as_view(), name='home'),
    path("decks_list/<slug:slug>", views.DecksView.as_view(), name='choose'),
    path("accounts/signup/", views.signup, name='signup'),
    path("accounts/logout/", views.logout_view, name='logout'),
    url(r'^send_email$', SendEmailView.as_view(), name='email_act'),
    path("account_activation_sent", activation_email_sent, name='email'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'
        ,activate, name='activate'),
    path('new-post/', new_deck, name='new_deck'),
    path('update_post/<str:pk>', update_deck, name='update_deck'),
    path('delete_post/<str:pk>', delete_deck, name='delete_deck')
]

