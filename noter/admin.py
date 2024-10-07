from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Note, Tag, NoteTag, UserPrefs, AuditLogs

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'user')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(NoteTag)
class NoteTagAdmin(admin.ModelAdmin):
    list_display = ('note_id', 'tag_id')


@admin.register(UserPrefs)
class UserPrefsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'theme', 'notifs_enabled')


@admin.register(AuditLogs)
class AuditLogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'action', 'action_time')
