from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import *
from karatekyokushin.views import *
from karateshotokan.views import *

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'system.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r"static/(?P<path>.*)$", "django.static.serve", {"document_root" : settings.STATIC_TEMPLATES}),
    #url(r"^media/(?P<path>.*)$", "django.static.serve", {"document_root" : settings.MEDIA_ROOT}, name="media"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^karatekyokushin/', KarateKyokushinMain, name='KarateKyokushinMain'),
    url(r'^karateshotokan/', KarateShotokanMain, name='KarateShotokanMain'),
    url(r'^createTournament/', createTournament, name='createTournament'),
    url(r'^createTeam/', createTeam, name='CreateTeam'),
    url(r'^signUp/', signUp, name='signUp'),
    url(r'^signIn/', signIn, name='signIn'),
    url(r'^logout/', logout, name='logout'),
    url(r'^tournament/(?P<tournament_id>\d+)/', tournament, name='tournament'),
    url(r'^kyoRandPlayers/(?P<tournament_id>\d+)/', kyoRandPlayers, name='kyoRandPlayers'),
    url(r'^kyo-category/(?P<category_id>\d+)/', kyoCategory, name='kyoCategory'),
    url(r'^kyoTournamentOrganization/(?P<tournament_id>\d+)/', kyoTournamentOrganization, name='kyoTournamentOrganization'),
    url(r'^team/(?P<team_id>\d+)/', team, name='team'),
    url(r'^userToAdd/(?P<user_id>\d+) (?P<team_id>\d+)/', userToAdd, name='userToAdd'),
    url(r'^playerToAdd/(?P<player_id>\d+) (?P<tournament_id>\d+)/', playerToAdd, name='playerToAdd'),
    url(r'^enterPlayerTour/(?P<player_id>\d+) (?P<tournament_id>\d+)/', enterPlayerTour, name='enterPlayerTour'),
    url(r'^deletePlayerTour/(?P<player_id>\d+) (?P<tournament_id>\d+)/', deletePlayerTour, name='deletePlayerTour'),
    url(r'^addPlayers/(?P<team_id>\d+)/', addPlayers, name='addPlayers'),
    url(r'^addPlayersToTournament/(?P<tournament_id>\d+)/', addPlayersToTournament, name='addPlayersToTournament'),
    url(r'^kyoAddPlayersToCategory/(?P<category_id>\d+)/', kyoAddPlayersToCategory, name='kyoAddPlayersToCategory'),
    url(r'^enterAllPlayersToTournament/(?P<tournament_id>\d+)(?P<user_id>\d+)/', enterAllPlayersToTournament, name='enterAllPlayersToTournament'),
    url(r'^enterPlayersTeamTour/(?P<team_id>\d+)(?P<tournament_id>\d+)/', enterPlayersTeamTour, name='enterPlayersTeamTour'),
    url(r'^updateTournament/(?P<tournament_id>\d+)/', updateTournament, name='updateTournament'),
    url(r'^kyoUpdateCategory/(?P<category_id>\d+)/', kyoUpdateCategory, name='kyoUpdateCategory'),
    url(r'^createCategoryKyo/(?P<tournament_id>\d+)/', createCategoryKyo, name='createCategoryKyo'),
    url(r'^enterForTournament/(?P<tournament_id>\d+)/ /(?P<user_id>\d+)/', enterForTournament, name='enterForTournament'),
    url(r'^playerToTeamAccept/(?P<player_id>\d+)/', playerToTeamAccept, name='playerToTeamAccept'),
    url(r'^playerToTournamentAccept/(?P<playerT_id>\d+)/', playerToTournamentAccept, name='playerToTournamentAccept'),
    url(r'^kyoPlayerToCategory/(?P<player_id>\d+)(?P<category_id>\d+)/', kyoPlayerToCategory, name='kyoPlayerToCategory'),
    url(r'^kyoDeletePlayerFromCategory/(?P<player_id>\d+)(?P<category_id>\d+)/', kyoDeletePlayerFromCategory, name='kyoDeletePlayerFromCategory'),
    url(r'^allPlayersTourAcceptByC/', allPlayersTourAcceptByC, name='allPlayersTourAcceptByC'),
    url(r'^allPlayersTourAcceptByM/', allPlayersTourAcceptByM, name='allPlayersTourAcceptByM'),
    url(r'^allTeamTourAcceptByM/(?P<team_id>\d+)/', allTeamTourAcceptByM, name='allTeamTourAcceptByM'),
    url(r'^user/', user, name='user'),
    url(r'^player/(?P<player_id>\d+)/', player, name='player'),
)
