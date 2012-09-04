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
    ipn = models.ForeignKey(ipn.models.PayPalIPN,
                            null=True, blank=True, editable=False)
    event = models.CharField(max_length=100, editable=False)
    amount = models.DecimalField(max_digits=64, decimal_places=2,
                                 null=True, blank=True, editable=False)
    comment = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('-timestamp',)

def _get_usersubscription_from_payment(payment):
    try:
        s = Subscription.objects.get(pk=payment.item_number)
    except Subscription.DoesNotExist:
        s = None

    try:
        u = User.objects.get(pk=payment.custom)
    except User.DoesNotExist:
        u = None

    if u is None or s is None:
        # We got an strange payment coming here, save it and return.
        SubscriptionTuple = namedtuple('SubscriptionTuple',
                                       ['user', 'subscription'])
        Transaction(user=u, subscription=s, ipn=payment,
                    event="unexpected, incomplete, or faulty response received",
                    amount=payment.mc_gross).save()
        return SubscriptionTuple(user=u, subscription=s)

    try:
        obj = UserSubscription.objects.get(subscription=s, user=u)
    except UserSubscription.DoesNotExist:
        obj = UserSubscription.objects.get_or_create(user=u,
                                                     subscription=s,
                                                     active=False)
    return obj

def paypal_successful_payment(sender, **kwargs):
    us = _get_usersubscription_from_payment(sender)
    if isinstance(us, UserSubscription):
        if sender.mc_gross == us.subscription.price:
            us.activate()
        else:
            # We got an incorrect payment here.
            Transaction(user=us.user, subscription=us.subscription, ipn=sender,
                        event='incorrect payment', amount=sender.mc_gross).save()

def paypal_flagged_payment(sender, **kwargs):
    us = _get_usersubscription_from_payment(sender):
    Transaction(user=us.user, subscription=us.subscription, ipn=sender,
                event='payment flagged', amount=sender.mc_gross
                ).save()

def paypal_subscription_signup(sender, **kwargs):
    us = _get_usersubscription_from_payment(sender)
    if isinstance(us, UserSubscription):
        us.signup()
        Transaction(user=us.user, subscription=us.subscription, ipn=sender,
                    event='subscription signup/modify', amount=sender.mc_gross
                    ).save()

def _deactivate_usersubscription_transaction(sender, instance, using):
    Transaction(user=sender.user, subscription=sender.subscription,
                event='subscription removed').save()

# TODO CONNECT SIGNAL

def paypal_subscription_cancel(sender, **kwargs):
    us = _get_usersubscription_from_payment(sender)
    if isinstance(us, UserSubscription):
        us.cancel()
        Transaction(user=us.user, subscription=us.subscription, ipn=sender,
                    event='subscription cancelled', amount=sender.mc_gross
                    ).save()
