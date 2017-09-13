from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^logout/$', views.logout_view, name='logout'),

    url(r'^add_poll/$', views.add_poll, name='add_poll'),
    url(r'^add_poll2/$', views.add_poll2, name='add_poll2'),

    url(r'^delete_poll/$', views.delete_poll, name='delete_poll'),

    url(r'^add_user/$', views.add_user, name='add_user'),
    url(r'^add_user2/$', views.add_user2, name='add_user2'),


    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]