# Models Imports
from .models import Chat, Message, LastMessage, ChatArchive

# Utility Imports
from django.contrib import admin

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(LastMessage)
admin.site.register(ChatArchive)
