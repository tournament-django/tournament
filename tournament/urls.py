from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views
from karatekyokushin import views
from karateshotokan import views
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r"static/(?P<path>.*)$", "django.views.static.serve", {"document_root" : settings.STATIC_TEMPLATES}, name="static"),
    url(r"^media/(?P<path>.*)$", "django.views.static.serve", {"document_root" : settings.MEDIA_ROOT}, name="media"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.home', name='home'),
    url(r'^karatekyokushin/', 'karatekyokushin.views.KarateKyokushinMain', name='KarateKyokushinMain'),
    url(r'^karateshotokan/', 'karateshotokan.views.KarateShotokanMain', name='KarateShotokanMain'),
    url(r'^create/', 'karatekyokushin.views.KarateKyokushinCreate', name='KarateKyokushinCreate'),
    url(r'^createTeam/', 'main.views.createTeam', name='CreateTeam'),
    url(r'^signUp/', 'main.views.signUp', name='signUp'),
    url(r'^signIn/', 'main.views.signIn', name='signIn'),
    url(r'^logout/', 'main.views.logout', name='logout'),
    url(r'^tournament/(?P<tournament_id>\d+)/', 'karatekyokushin.views.tournament', name='tournament'),
    url(r'^kyoRandPlayers/(?P<tournament_id>\d+)/', 'karatekyokushin.views.kyoRandPlayers', name='kyoRandPlayers'),
    url(r'^kyo-category/(?P<category_id>\d+)/', 'karatekyokushin.views.kyoCategory', name='kyoCategory'),
    url(r'^tournamentOrganization/(?P<tournament_id>\d+)/', 'karatekyokushin.views.tournamentOrganization', name='tournamentOrganization'),
    url(r'^team/(?P<team_id>\d+)/', 'main.views.team', name='team'),
    url(r'^userToAdd/(?P<user_id>\d+) (?P<team_id>\d+)/', 'main.views.userToAdd', name='userToAdd'),
    url(r'^playerToAdd/(?P<player_id>\d+) (?P<tournament_id>\d+)/', 'karatekyokushin.views.playerToAdd', name='playerToAdd'),
    url(r'^enterPlayerTour/(?P<player_id>\d+) (?P<tournament_id>\d+)/', 'karatekyokushin.views.enterPlayerTour', name='enterPlayerTour'),
    url(r'^deletePlayerTour/(?P<player_id>\d+) (?P<tournament_id>\d+)/', 'karatekyokushin.views.deletePlayerTour', name='deletePlayerTour'),
    url(r'^addPlayers/(?P<team_id>\d+)/', 'main.views.addPlayers', name='addPlayers'),
    url(r'^addPlayersToTournament/(?P<tournament_id>\d+)/', 'karatekyokushin.views.addPlayersToTournament', name='addPlayersToTournament'),
    url(r'^kyoAddPlayersToCategory/(?P<category_id>\d+)/', 'karatekyokushin.views.kyoAddPlayersToCategory', name='kyoAddPlayersToCategory'),
    url(r'^enterAllPlayersToTournament/(?P<tournament_id>\d+)(?P<user_id>\d+)/', 'main.views.enterAllPlayersToTournament', name='enterAllPlayersToTournament'),
    url(r'^enterPlayersTeamTour/(?P<team_id>\d+)(?P<tournament_id>\d+)/', 'main.views.enterPlayersTeamTour', name='enterPlayersTeamTour'),
    url(r'^updateTournament/(?P<tournament_id>\d+)/', 'main.views.updateTournament', name='updateTournament'),
    url(r'^kyoUpdateCategory/(?P<category_id>\d+)/', 'karatekyokushin.views.kyoUpdateCategory', name='kyoUpdateCategory'),
    url(r'^createCategoryKyo/(?P<tournament_id>\d+)/', 'karatekyokushin.views.createCategoryKyo', name='createCategoryKyo'),
    url(r'^enterForTournament/(?P<tournament_id>\d+)/ /(?P<user_id>\d+)/', 'main.views.enterForTournament', name='enterForTournament'),
    url(r'^playerToTeamAccept/(?P<player_id>\d+)/', 'main.views.playerToTeamAccept', name='playerToTeamAccept'),
    url(r'^playerToTournamentAccept/(?P<playerT_id>\d+)/', 'karatekyokushin.views.playerToTournamentAccept', name='playerToTournamentAccept'),
    url(r'^kyoPlayerToCategory/(?P<player_id>\d+)(?P<category_id>\d+)/', 'karatekyokushin.views.kyoPlayerToCategory', name='kyoPlayerToCategory'),
    url(r'^kyoDeletePlayerFromCategory/(?P<player_id>\d+)(?P<category_id>\d+)/', 'karatekyokushin.views.kyoDeletePlayerFromCategory', name='kyoDeletePlayerFromCategory'),
    url(r'^allPlayersTourAcceptByC/', 'main.views.allPlayersTourAcceptByC', name='allPlayersTourAcceptByC'),
    url(r'^allPlayersTourAcceptByM/', 'main.views.allPlayersTourAcceptByM', name='allPlayersTourAcceptByM'),
    url(r'^allTeamTourAcceptByM/(?P<team_id>\d+)/', 'main.views.allTeamTourAcceptByM', name='allTeamTourAcceptByM'),
    url(r'^user/', 'main.views.user', name='user'),
    url(r'^player/(?P<player_id>\d+)/', 'karatekyokushin.views.player', name='player'),
)
