from collections import namedtuple
from django.db import models
from django.contrib.auth.models import User

from subscription.models import Subscription, UserSubscription

class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    subscription = models.ForeignKey(Subscription,
                                     null=True, blank=True, editable=False)
    user = models.ForeignKey(User,
                             null=True, blank=True, editable=False)
    event = models.CharField(max_length=100, editable=False)
    amount = models.DecimalField(max_digits=64, decimal_places=2,
                                 null=True, blank=True, editable=False)
    comment = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('-timestamp',)

def _deactivate_usersubscription_transaction(sender, instance, using):
    Transaction(user=sender.user, subscription=sender.subscription,
                event='subscription removed').save()

# TODO CONNECT SIGNAL
