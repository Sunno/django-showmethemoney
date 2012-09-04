from models import PaypalTransaction
from utils import _get_usersubscription_from_payment

def _paypal_successful_payment(sender, **kwargs):
    us = _get_usersubscription_from_payment(sender)
    if isinstance(us, UserSubscription):
        if sender.mc_gross == us.subscription.price:
            us.activate()
            PaypalTransaction(user=us.user, subscription=us.subscription,
                              ipn=sender, event='payment received',
                              amount=sender.mc.gross).save()
        else:
            # We got an incorrect payment here.
            PaypalTransaction(user=us.user, subscription=us.subscription,
                              ipn=sender, event='incorrect payment',
                              amount=sender.mc_gross).save()

def _paypal_flagged_payment(sender, **kwargs):
    us = _get_usersubscription_from_payment(sender):
    PaypalTransaction(user=us.user, subscription=us.subscription, ipn=sender,
                event='payment flagged', amount=sender.mc_gross
                ).save()

def _paypal_subscription_signup(sender, **kwargs):
    us = _get_usersubscription_from_payment(sender)
    if isinstance(us, UserSubscription):
        us.signup()
        PaypalTransaction(user=us.user, subscription=us.subscription,
                          ipn=sender, event='subscription signup/modify',
                          amount=sender.mc_gross).save()

def _paypal_subscription_cancel(sender, **kwargs):
    us = _get_usersubscription_from_payment(sender)
    if isinstance(us, UserSubscription):
        us.cancel()
        PaypalTransaction(user=us.user, subscription=us.subscription,
                          ipn=sender, event='subscription cancelled',
                          amount=sender.mc_gross).save()
