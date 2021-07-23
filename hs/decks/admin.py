from django.contrib import admin
from django.contrib.auth.models import User
from django.shortcuts import render

from .forms import SendEmailForm
from .models import Arthetype, Deck, Deck_Picture, Deck_Review, Player

admin.site.register(Arthetype)
admin.site.register(Deck)
admin.site.register(Deck_Picture)
admin.site.register(Deck_Review)
admin.site.register(Player)
admin.site.unregister(User)
# admin.site.register(Decks_Names)


@admin.register(User)
class CustomAdmin(admin.ModelAdmin):
    actions = ['send_email', ]

    def send_email(self, request, queryset):
        form = SendEmailForm(initial={'users': queryset})
        return render(request, 'mail/send_email.html', {'form': form})
