import time
import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from paypal.interface import PayPalInterface
from django.http import HttpResponse
from forms import PayPalIPNForm
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.sites.models import Site
# from django.views.generic import FormView
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
import subscription.utils as subscription_utils
from models import PayPalUserSubscription
#from paypal.pro.views import PayPalPro
DOMAIN = Site.objects.get_current().domain

#from forms import SelectSubscriptionForm
def _get_express_checkout_dict(subscription, user):
    """Returns a subscription dict for use with PPP"""
    return dict(
        # Required fields
        # where to go after we authorize
        RETURNURL='http://%s%s' % (DOMAIN,
                                    reverse('subscription:payment_authorized')),
        # where to go in case we cancel
        CANCELURL='http://%s%s' % (DOMAIN,
                                    reverse('subscription:payment_canceled')),
        REQCONFIRMSHIPPING=0, # no shipping
        NOSHIPPING=1, # ditto, no shipping
        EMAIL=user.email, # Email of the user for sign up in paypal
        PAYMENTREQUEST_0_AMT=0, #price.subscriptiton, # amount to pay
        PAYMENTREQUEST_0_ITEMAMT=0, #subscription.price, # sum of all digital goods
        PAYMENTREQUEST_0_DESC=subscription.description, # description of the item
        PAYMENTREQUEST_0_CUSTOM=user.pk, # user whho's buying
        PAYMENTREQUEST_0_INVNUM=subscription.pk,
        #PAYMENTREQUEST_n_NOTIFYURL # maybe ipn
        L_BILLINGAGREEMENTDESCRIPTION0='Jim Venetos Golf Academy Membership: %s' % subscription.description,
        L_BILLINGTYPE0='RecurringPayments',
    )

def create_recurring_profile_handler(request):
    """We will return a tuple where the first element is the dict that
    should be passed to PayPal CreateRecurringPaymentsProfile method and the
    second one is a PayPalUserSubscription object already set up that matches
    the data on the dict."""
    token = request.session['paypal_token']
    subscription = request.session['paypal_subscription']
    user = request.user
    profile = user.get_profile()
    upgrading = request.session['paypal_upgrading']
    us = request.session['paypal_current']
    time_obj = datetime.datetime.now()
    trial = False
    new_us = PayPalUserSubscription(
        user=user, subscription=subscription
    )
    if upgrading and us is not None:
        # We set the Trial time as the time left on the current user
        # subscription
        delta_days = (us.expires-datetime.datetime.now().date()).days
        print delta_days
        if delta_days > 0:
            print 'Adding trial time from our current subscription'
            trial = True
            trial_dict = dict(
                TRIALBILLINGPERIOD='Day',
                TRIALBILLINGFREQUENCY=delta_days,
                TRIALTOTALBILLINGCYCLES=1,
                TRIALAMT=0
            )
            new_us.expires = subscription_utils.extend_date_by(
                new_us.expires,
                delta_days,
                'D'
            )
            print trial_dict
    elif not profile.had_trial:
        # The user is not upgrading and hasn't had his trial period.'
        trial = True
        trial_dict = dict(
            TRIALBILLINGPERIOD=subscription.get_trial_unit_display(),
            TRIALBILLINGFREQUENCY=1,
            TRIALTOTALBILLINGCYCLES=1,
            TRIALAMT=0
        )
        new_us.expires = subscription_utils.extend_date_by(
            new_us.expires,
            subscription.trial_period,
            subscription.trial_unit
        )
    else:
        # No trial.
        pass

    the_dict = dict(
        TOKEN=token,
        PROFILESTARTDATE=time_obj.strftime('%Y-%m-%dT%H:%M:%SZ'),
        DESC='Jim Venetos Golf Academy Membership: %s' % subscription.description,
        BILLINGPERIOD=subscription.get_recurrence_unit_display(),
        BILLINGFREQUENCY=1,
        AMT=subscription.price,
        MAXFAILEDPAYMENTS=3,
    )
    if trial:
        the_dict.update(trial_dict)

    return (the_dict, new_us)

def _get_express_checkout_details(token):
    return _get_paypal_interface().get_express_checkout_details(TOKEN=token)

def _get_paypal_interface():
    return PayPalInterface(
        API_USERNAME=settings.PAYPAL_API_USERNAME,
        API_PASSWORD=settings.PAYPAL_API_PASSWORD,
        API_SIGNATURE=settings.PAYPAL_API_SIGNATURE,
        API_ENVIRONMENT=settings.PAYPAL_API_ENVIRONMENT,
    )


@csrf_exempt
def ipn(request):
    """Simple IPN handler"""
    ipn_obj = None
    data = request.POST.copy()
    date_fields = ('time_created', 'payment_date', 'next_payment_date',
                   'subscr_date', 'subscr_effective')
    for date_field in date_fields:
        if data.get(date_field) == 'N/A':
            del data[date_field]

    form = PayPalIPNForm(data)
    if form.is_valid():
        form.initialize(request)
        # TODO: SSL secrets.
        ipn_obj = form.save(commit=False)
        ipn_obj.from_view = 'notify'
        # make ipaddress None because https://code.djangoproject.com/ticket/5622
        if ipn_obj.ipaddress == '':
            ipn_obj.ipaddress = None
        ipn_obj.save()
        ipn_obj.send_signals()
        print 'IPN request saved'
    else:
        print 'ignoring IPN request'
        print form.errors
    print 'values = %s' % request.POST
    return HttpResponse("OKAY")
