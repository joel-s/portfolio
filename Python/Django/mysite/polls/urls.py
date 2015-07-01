from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name='index'),
    url(r'^details/$', views.detailed_index_view, name='detailed_index'),
    url(r'^dynamic/$', views.DynamicIndexView.as_view(), name='dynamic_index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
