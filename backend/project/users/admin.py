# Models Imports
from project.users.models import EndUser, Connection, Note, PeopleUnfollow, Setting, Website


# Utility Imports
from django.contrib import admin


class EndUserAdmin(admin.ModelAdmin):
    list_display = ["img"]

    def img(self, obj):
        return obj.avatar


admin.site.register(EndUser, EndUserAdmin)
admin.site.register(Connection)
admin.site.register(Note)
admin.site.register(PeopleUnfollow)
admin.site.register(Setting)
admin.site.register(Website)
