from django.contrib.auth.models import User
from subscription.models import Subscription

from models import PaypalTransaction

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
        PaypalTransaction(user=u, subscription=s, ipn=payment,
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
