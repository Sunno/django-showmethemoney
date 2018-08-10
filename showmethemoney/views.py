from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView
from django.forms.util import ErrorList
from django.contrib import messages
import paypal

from django.core.mail import EmailMessage
from django.conf import settings

from showmethemoney.forms import SelectSubscriptionForm
from showmethemoney.providers.paypal.models import PayPalTransaction,\
    PayPalUserSubscription
import showmethemoney.providers.paypal.views as paypal_views
from subscription.models import Subscription


class CancellableMixin(object):
    def cancel(self, interface, current):
        try:
            interface.manage_recurring_payments_profile_status(
                current.profileid, 'Cancel')
        except paypal.exceptions.PayPalAPIResponseError as e:
            if e.error_code != 11556:
                # this error code is returned when it's already cancelled
                raise
        current.cancel()


class CancelSubscriptionView(CancellableMixin, TemplateView):
    template_name = 'showmethemoney/cancel.html'

    def post(self, request, *args, **kwargs):
        """This is method is triggered when the user accepts that he
        wants to cancel his current subscription"""
        current = self.request.user.get_active_paypal_subscription()
        if current is not None and not current.cancelled:
            self.cancel(paypal_views._get_paypal_interface(),
                        current)
            messages.success(
                self.request,
                'Your subscription has been successfully cancelled.')
        return HttpResponseRedirect(reverse('subscription:change'))


class ChangeSubscriptionView(FormView):
    form_class = SelectSubscriptionForm
    template_name = 'showmethemoney/create.html'

    def form_valid(self, form):
        """We will proceed with the express checkout here."""
        # First we will check that we can indeed, upgrade to this
        # subscription type.
        self.user = self.request.user
        self.interface = paypal_views._get_paypal_interface()
        us = self.user.get_active_paypal_subscription()
        if us is not None and not us.expired and not us.cancelled and us.valid:
            errors = us.try_change(form.cleaned_data['subscription'])
            if errors:
                form._errors.setdefault('subscription', ErrorList(errors))
                return self.form_invalid(form)
            # If we get this far it means we are updating a
            # subscription.  We will mark it for deletion, delete it
            # after we come back from paypal, and then proceed with
            # the usual process.
        return self.subscribe(form, us)

    def subscribe(self, form, us=None):
        '''Create a brand new subscription for this user.'''
        # we begin the express checkout process
        try:
            response = self.interface.set_express_checkout(
                **paypal_views._get_express_checkout_dict(
                    subscription=form.cleaned_data['subscription'],
                    user=self.user
                )
            )
        except paypal.exceptions.PayPalAPIResponseError as e:
            email = EmailMessage(
                'PayPalError',
                e,
                'contact@jimvenetosgolfacademy.com',
                [admin[1] for admin in settings.ADMINS])
            email.send()
            messages.error(
                self.request,
                'There has been an error with your request, please try again.')
            return HttpResponseRedirect(reverse('subscription:change'))

        token = response.token
        self.request.session['paypal_token'] = token
        self.request.session['paypal_active_checkout'] = True
        self.request.session['paypal_subscription'] = form.cleaned_data[
            'subscription'].pk
        self.request.session['paypal_upgrading'] = us is not None
        self.request.session['paypal_current'] = us.pk if us is not None \
            else None
        # We redirect to PayPal! Good luck.
        return HttpResponseRedirect(
            self.interface.generate_express_checkout_redirect_url(token)
        )


class PaymentAuthorizedView(CancellableMixin, TemplateView):
    template_name = 'showmethemoney/authorized.html'
    payment_successful_url = 'class_list'
    payment_invalid_url = 'subscription:change'

    def get_context_data(self, **kwargs):
        ctx = super(PaymentAuthorizedView, self).get_context_data(**kwargs)
        ctx['checkout_details'] = paypal_views._get_express_checkout_details(
            self.request.session['paypal_token']
        )
        subscription_id = self.request.session['paypal_subscription'] or\
            self.request.session['subscription']
        ctx['subscription'] = Subscription.objects.get(
            pk=subscription_id
        )
        return ctx

    def dispatch(self, request, *args, **kwargs):
        if request.session.has_key('paypal_active_checkout') and \  # noqa
           request.session['paypal_active_checkout']:
            return super(PaymentAuthorizedView, self).dispatch(request, *args,
                                                               **kwargs)
        else:
            return HttpResponseRedirect(reverse('subscription:change'))

    def post(self, request, *args, **kwargs):
        # User clicked Continue
        interface = paypal_views._get_paypal_interface()
        subscription = Subscription.objects.get(
            pk=self.request.session['paypal_subscription'])
        recurr_dict, us = paypal_views.create_recurring_profile_handler(
            self.request)
        success_msg = 'We have successfully updated your subscription status. Welcome to Jim Venetos Golf Academy!'  # noqa
        try:
            # Check whether or not we have to delete our current subscription.
            if self.request.session['paypal_upgrading']:
                current = PayPalUserSubscription.objects.get(
                    pk=self.request.session['paypal_current']
                )
                self.cancel(
                    interface, current
                )
            response = interface.create_recurring_payments_profile(
                **recurr_dict
            )
        except paypal.exceptions.PayPalAPIResponseError as e:
            email = EmailMessage(
                'PayPalError', str(e),
                'contact@jimvenetosgolfacademy.com',
                [admin[1] for admin in settings.ADMINS])
            email.send()
            messages.error(
                self.request,
                'There has been an error with your request, please try again.')
            return HttpResponseRedirect(reverse(self.payment_invalid_url))

        if response.profilestatus == 'ActiveProfile' or \
           response.profilestatus == 'PendingProfile':
            # We got a valid response here. Let's subscribe our user.'
            us.profileid = response.profileid
            us.signup()
            profile = self.request.user.profile
            if profile.had_trial:
                # We will wait until we get a payment notification before
                # we extend the subscription period. By default
                # signup() method activates the account and will be able to
                # use our services for a grace period until we get notified.
                PayPalTransaction(
                    user=self.request.user, subscription=subscription,
                    event='subscription create/modify (waiting for payment)',
                    amount=subscription.price).save()
            else:
                # This is the first time the user registers with us. We will
                # award our trial period.
                success_msg = 'Welcome! Get started by selecting below the type of golfer you want to be. After that watch the "Welcome to the JVGA" video to begin your journey!'  # noqa
                PayPalTransaction(
                    user=self.request.user, subscription=subscription,
                    event='subscription create/modify (with trial)',
                    amount=0).save()
                profile.had_trial = True
                profile.save()

            url = self.payment_successful_url
            messages.success(self.request, success_msg)
        else:
            # error, get out of here and restart.
            url = self.payment_invalid_url
            messages.error(self.request,
                           "Invalid payment. Please try again.")
        # Clean up and get out of here.
        del self.request.session['paypal_token']
        del self.request.session['paypal_subscription']
        del self.request.session['paypal_active_checkout']
        del self.request.session['paypal_upgrading']
        del self.request.session['paypal_current']
        return HttpResponseRedirect(reverse(url))
