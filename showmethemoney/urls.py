from django.conf.urls.defaults import patterns, url, include
from django.views.generic import TemplateView

from views import (ChangeSubscriptionView, PaymentAuthorizedView,
                   CancelSubscriptionView)
from showmethemoney.providers.paypal.views import ipn
urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(
        template_name='showmethemoney/manage.html'
    ),
        name='manage'),
    url(r'^cancel/$', CancelSubscriptionView.as_view(),
        name='cancel'),
    url(r'^ipn', ipn, name='ipn'),
    url(r'^create/$', ChangeSubscriptionView.as_view(),
        name='change'),
    url(r'^create/authorized', PaymentAuthorizedView.as_view(),
        name='payment_authorized'),
    url(r'^create/canceled', TemplateView.as_view(
        template_name='showmethemoney/canceled.html'
    ),
        name='payment_canceled'),
    # url(r'^cancel/$', cancel_subscription, name='subscription:cancel'),
)
