from django.conf.urls.defaults import patterns, url
from views import ipn

urlpatterns = patterns(
    url(r'^ipn/$', ipn, name='ipn'),
)
