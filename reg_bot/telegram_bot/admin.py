from django.contrib import admin
from .models import Confirmation, Game, Team


@admin.register(Confirmation)
class ConfirmationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'number',
        'date',
        'place',
        'get_team')

    def get_team(self, obj):
        return "\n".join([t.name for t in obj.team.all()])


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'captain',
        'phone',
        'email',
        'members')
