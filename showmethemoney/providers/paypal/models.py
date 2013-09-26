from django.db import models
from django.dispatch import receiver

#from paypal.standard.ipn.models import PayPalIPN
from showmethemoney.models import Transaction
from signals import (payment_was_flagged, recurring_create,
                     recurring_expired, recurring_payment,
                     recurring_skipped, recurring_cancelled)
from subscription.models import UserSubscription
from django.contrib import auth
import signals
#from utils import _get_usersubscription_from_ipn

ST_PP_ACTIVE = 'Active'
ST_PP_CANCELLED = 'Cancelled'
ST_PP_CLEARED = 'Cleared'
ST_PP_COMPLETED = 'Completed'
ST_PP_DENIED = 'Denied'
ST_PP_PAID = 'Paid'
ST_PP_PENDING = 'Pending'
ST_PP_PROCESSED = 'Processed'
ST_PP_REFUSED = 'Refused'
ST_PP_REVERSED = 'Reversed'
ST_PP_REWARDED = 'Rewarded'
ST_PP_UNCLAIMED = 'Unclaimed'
ST_PP_UNCLEARED = 'Uncleared'


class PayPalIPN(models.Model):
    PAYMENT_STATUS_CHOICES = (ST_PP_ACTIVE, ST_PP_CANCELLED, ST_PP_CLEARED,
                              ST_PP_COMPLETED, ST_PP_DENIED, ST_PP_PAID,
                              ST_PP_PENDING, ST_PP_PROCESSED, ST_PP_REFUSED,
                              ST_PP_REVERSED, ST_PP_REWARDED, ST_PP_UNCLAIMED,
                              ST_PP_UNCLEARED)
    # hand picked from ipn.pdf!
    # basic info
    business = models.CharField(max_length=127, blank=True, help_text="Email where the money was sent.")
    receiver_email = models.EmailField(max_length=127, blank=True)
    receiver_id = models.CharField(max_length=127, blank=True)  # 258DLEHY2BDK6
    # transaction information
    payment_status = models.CharField(max_length=9, blank=True)
    payment_type = models.CharField(max_length=7, blank=True)
    payment_date = models.DateTimeField(blank=True, null=True, help_text="HH:MM:SS DD Mmm YY, YYYY PST")
    txn_id = models.CharField("Transaction ID", max_length=19, blank=True,
                              help_text="PayPal transaction ID.", db_index=True)
    initial_payment_amount = models.DecimalField(max_digits=64, decimal_places=2,
                                                 default=0, blank=True,
                                                 null=True)
    initial_payment_txn_id = models.CharField("Initial Transaction ID", max_length=19, blank=True,
                                              help_text="PayPal transaction ID.")
    txn_type = models.CharField("Transaction Type", max_length=128, blank=True,
                                help_text="PayPal transaction type.")
    # currency and exchange
    mc_gross = models.DecimalField(max_digits=64, decimal_places=2, default=0,
                                   blank=True, null=True)
    mc_currency = models.CharField(max_length=32, default="USD", blank=True)
    mc_fee = models.DecimalField(max_digits=64, decimal_places=2, default=0,
                                 blank=True, null=True)

    payment_gross = models.DecimalField(max_digits=64, decimal_places=2, default=0, blank=True, null=True)
    # missing payment_code, payment_fee
    # basic information
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    address_country = models.CharField(max_length=64, blank=True)
    address_city = models.CharField(max_length=40, blank=True)
    address_country_code = models.CharField(max_length=64, blank=True, help_text="ISO 3166")
    address_name = models.CharField(max_length=128, blank=True)
    address_state = models.CharField(max_length=40, blank=True)
    address_status = models.CharField(max_length=11, blank=True)
    address_street = models.CharField(max_length=200, blank=True)
    address_zip = models.CharField(max_length=20, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    payer_email = models.CharField(max_length=127, blank=True)
    payer_id = models.CharField(max_length=13, blank=True)
    residence_country = models.CharField(max_length=2, blank=True)
    # recurring info
    amount = models.DecimalField(max_digits=64, decimal_places=2, default=0,
                                 blank=True, null=True)
    amount_per_cycle = models.DecimalField(max_digits=64, decimal_places=2,
                                           default=0, blank=True, null=True)

    next_payment_date = models.DateTimeField(blank=True, null=True,
                                             help_text="HH:MM:SS DD Mmm YY, YYYY PST")
    outstanding_balance = models.DecimalField(max_digits=64, decimal_places=2,
                                              default=0, blank=True, null=True)
    payment_cycle= models.CharField(max_length=32, blank=True) #Monthly
    period_type = models.CharField(max_length=32, blank=True)
    product_name = models.CharField(max_length=128, blank=True)
    product_type= models.CharField(max_length=128, blank=True)
    profile_status = models.CharField(max_length=32, blank=True)
    recurring_payment_id = models.CharField(max_length=128, blank=True)  # I-FA4XVST722B9
    rp_invoice_id= models.CharField(max_length=127, blank=True)  # 1335-7816-2936-1451
    time_created = models.DateTimeField(blank=True, null=True,
                                        help_text="HH:MM:SS DD Mmm YY, YYYY PST")
    # other information

    notify_version = models.DecimalField(max_digits=64, decimal_places=2, default=0, blank=True, null=True)
    charset=models.CharField(max_length=32, blank=True)
    # recurring_payment_id = models.CharField(max_length=128, blank=True)  # I-FA4XVST722B9
    # custom = models.CharField(max_length=255, blank=True)

    # Recurring Payments Variables

    # Non-PayPal Variables - full IPN/PDT query and time fields.
    ipaddress = models.IPAddressField(blank=True, null=True) # null=True because https://code.djangoproject.com/ticket/5622
    flag = models.BooleanField(default=False, blank=True)
    flag_code = models.CharField(max_length=16, blank=True)
    flag_info = models.TextField(blank=True)
    query = models.TextField(blank=True)  # What Paypal sent to us initially
    response = models.TextField(blank=True)  # What we got back from our request
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Where did it come from?
    from_view = models.CharField(max_length=6, null=True, blank=True)

    def is_transaction(self):
        return len(self.txn_id) > 0

    def is_recurring(self):
        return len(self.recurring_payment_id) > 0

    # def is_subscription_cancellation(self):
    #     return self.txn_type == "subscr_cancel"

    # def is_subscription_end_of_term(self):
    #     return self.txn_type == "subscr_eot"

    # def is_subscription_modified(self):
    #     return self.txn_type == "subscr_modify"

    # def is_subscription_signup(self):
    #     return self.txn_type == "subscr_signup"

    def is_recurring_create(self):
        return self.txn_type == "recurring_payment_profile_created"

    def is_recurring_payment(self):
        return self.txn_type == "recurring_payment"

    def is_recurring_expired(self):
        return self.txn_type == "recurring_payment_profile_expired"

    def is_recurring_skipped(self):
        return self.txn_type == "recurring_payment_skipped"

    def is_recurring_cancelled(self):
        return self.txn_type == 'recurring_payment_profile_cancel'

    def send_signals(self):
        """Shout for the world to hear whether a txn was successful."""

        # Don't do anything if we're not notifying!
        if self.from_view != 'notify':
            return

        # # Transaction signals:
        # if self.is_transaction():
        if self.flag:
            payment_was_flagged.send(sender=self)
        #     else:
        #         payment_was_successful.send(sender=self)
        # recurring payments
        if self.is_recurring():
            if self.is_recurring_create():
                recurring_create.send(sender=self)
            elif self.is_recurring_payment():
                recurring_payment.send(sender=self)
            elif self.is_recurring_expired():
                recurring_expired.send(sender=self)
            elif self.is_recurring_skipped():
                recurring_skipped.send(sender=self)
            elif self.is_recurring_cancelled():
                recurring_cancelled.send(sender=self)
        # Subscription signals:
        # else:
        #     if self.is_subscription_cancellation():
        #         subscription_cancel.send(sender=self)
        #     elif self.is_subscription_signup():
        #         subscription_signup.send(sender=self)
        #     elif self.is_subscription_end_of_term():
        #         subscription_eot.send(sender=self)`q`
        #     elif self.is_subscription_modified():
        #         subscription_modify.send(sender=self)

    def set_flag(self, info, code=None):
        """Sets a flag on the transaction and also sets a reason."""
        self.flag = True
        self.flag_info += info
        if code is not None:
            self.flag_code = code

class PayPalTransaction(Transaction):
    ipn = models.ForeignKey(PayPalIPN, null=True, blank=True,
                            editable=False)
    def __unicode__(self):
        return "%s - %s" % (self.event, self.timestamp)

class PayPalUserSubscription(UserSubscription):
    profileid = models.CharField(max_length=128)

def __user_get_active_subscription(user):
    try:
        return PayPalUserSubscription.objects.get(user=user, active=True)
    except PayPalUserSubscription.DoesNotExist:
        return None
auth.models.User.add_to_class('get_active_paypal_subscription',__user_get_active_subscription)

def _get_usersubscription_from_ipn(payment):
    """Get a UserSubscription object or in case we got an strange
    response object coming in we return a UserSubscription like object
    to be able to log"""
    us = PayPalUserSubscription.objects.filter(profileid=payment.recurring_payment_id)
    return us.exists(), us


def _paypal_recurring_expired(sender, **kwargs):
    print 'doing expired, skipped'
    exists, us = _get_usersubscription_from_ipn(sender)
    if exists:
        us = us.get()
        us.cancel()
        PayPalTransaction(user=us.user, subscription=us.subscription,
                          ipn=sender, event='subscription cancelled/expired or skipped',
                          amount=sender.mc_gross).save()

def _paypal_recurring_payment(sender, **kwargs):
    print 'doing payment'
    exists, us = _get_usersubscription_from_ipn(sender)
    if exists:
        us = us.get()
        if sender.mc_gross == us.subscription.price:
            us.activate() # this extends by the subscription recurrence unit
            PayPalTransaction(user=us.user, subscription=us.subscription,
                              ipn=sender, event='subscription payment',
                              amount=sender.mc_gross).save()
        else:
            # incorrect payment
            PayPalTransaction(user=us.user, subscription=us.subscription,
                              ipn=sender, event='incorrect subscription payment',
                              amount=sender.mc_gross).save()

signals.recurring_payment.connect(_paypal_recurring_payment)
signals.recurring_expired.connect(_paypal_recurring_expired)
signals.recurring_skipped.connect(_paypal_recurring_expired)
signals.recurring_cancelled.connect(_paypal_recurring_expired)

