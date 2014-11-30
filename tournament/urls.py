from django.conf.urls import patterns, include, url

from django.contrib import admin
from main import views
from karatekyokushin import views2
from karateshotokan import views3

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r"static/(?P<path>.*)$", "django.views.static.serve", {"document_root" : settings.STATIC_TEMPLATES}),
    url(r"^media/(?P<path>.*)$", "django.views.static.serve", {"document_root" : settings.MEDIA_ROOT}, name="media"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^karatekyokushin/', views2.KarateKyokushinMain, name='KarateKyokushinMain'),
    url(r'^karateshotokan/', views3.KarateShotokanMain, name='KarateShotokanMain'),
    url(r'^create/', views2.KarateKyokushinCreate, name='KarateKyokushinCreate'),
    url(r'^createTeam/', views.createTeam, name='CreateTeam'),
    url(r'^signUp/', views.signUp, name='signUp'),
    url(r'^signIn/', views.signIn, name='signIn'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^tournament/(?P<tournament_id>\d+)/', views2.tournament, name='tournament'),
    url(r'^kyoRandPlayers/(?P<tournament_id>\d+)/', views2.kyoRandPlayers, name='kyoRandPlayers'),
    url(r'^kyo-category/(?P<category_id>\d+)/', views2.kyoCategory, name='kyoCategory'),
    url(r'^tournamentOrganization/(?P<tournament_id>\d+)/', views2.tournamentOrganization, name='tournamentOrganization'),
    url(r'^team/(?P<team_id>\d+)/', views.team, name='team'),
    url(r'^userToAdd/(?P<user_id>\d+) (?P<team_id>\d+)/', views.userToAdd, name='userToAdd'),
    url(r'^playerToAdd/(?P<player_id>\d+) (?P<tournament_id>\d+)/', views2.playerToAdd, name='playerToAdd'),
    url(r'^enterPlayerTour/(?P<player_id>\d+) (?P<tournament_id>\d+)/', views2.enterPlayerTour, name='enterPlayerTour'),
    url(r'^deletePlayerTour/(?P<player_id>\d+) (?P<tournament_id>\d+)/', views2.deletePlayerTour, name='deletePlayerTour'),
    url(r'^addPlayers/(?P<team_id>\d+)/', views.addPlayers, name='addPlayers'),
    url(r'^addPlayersToTournament/(?P<tournament_id>\d+)/', views2.addPlayersToTournament, name='addPlayersToTournament'),
    url(r'^kyoAddPlayersToCategory/(?P<category_id>\d+)/', views2.kyoAddPlayersToCategory, name='kyoAddPlayersToCategory'),
    url(r'^enterAllPlayersToTournament/(?P<tournament_id>\d+)(?P<user_id>\d+)/', views.enterAllPlayersToTournament, name='enterAllPlayersToTournament'),
    url(r'^enterPlayersTeamTour/(?P<team_id>\d+)(?P<tournament_id>\d+)/', views.enterPlayersTeamTour, name='enterPlayersTeamTour'),
    url(r'^updateTournament/(?P<tournament_id>\d+)/', views.updateTournament, name='updateTournament'),
    url(r'^kyoUpdateCategory/(?P<category_id>\d+)/', views2.kyoUpdateCategory, name='kyoUpdateCategory'),
    url(r'^createCategoryKyo/(?P<tournament_id>\d+)/', views2.createCategoryKyo, name='createCategoryKyo'),
    url(r'^enterForTournament/(?P<tournament_id>\d+)/ /(?P<user_id>\d+)/', views.enterForTournament, name='enterForTournament'),
    url(r'^playerToTeamAccept/(?P<player_id>\d+)/', views.playerToTeamAccept, name='playerToTeamAccept'),
    url(r'^playerToTournamentAccept/(?P<playerT_id>\d+)/', views2.playerToTournamentAccept, name='playerToTournamentAccept'),
    url(r'^kyoPlayerToCategory/(?P<player_id>\d+)(?P<category_id>\d+)/', views2.kyoPlayerToCategory, name='kyoPlayerToCategory'),
    url(r'^kyoDeletePlayerFromCategory/(?P<player_id>\d+)(?P<category_id>\d+)/', views2.kyoDeletePlayerFromCategory, name='kyoDeletePlayerFromCategory'),
    url(r'^allPlayersTourAcceptByC/', views.allPlayersTourAcceptByC, name='allPlayersTourAcceptByC'),
    url(r'^allPlayersTourAcceptByM/', views.allPlayersTourAcceptByM, name='allPlayersTourAcceptByM'),
    url(r'^allTeamTourAcceptByM/(?P<team_id>\d+)/', views.allTeamTourAcceptByM, name='allTeamTourAcceptByM'),
    url(r'^user/', views.user, name='user'),
    url(r'^player/(?P<player_id>\d+)/', views2.player, name='player'),
)
