import urllib2
from django import forms
from django.conf import settings
from models import PayPalIPN, PayPalUserSubscription
PAYPAL_DATE_FORMAT = ("%H:%M:%S %b. %d, %Y PST",
                      "%H:%M:%S %b. %d, %Y PDT",
                      "%H:%M:%S %d %b %Y PST",
                      "%H:%M:%S %d %b %Y PDT",
                      "%H:%M:%S %b %d, %Y PST",
                      "%H:%M:%S %b %d, %Y PDT",)

class PayPalIPNForm(forms.ModelForm):
    payment_date = forms.DateTimeField(input_formats=PAYPAL_DATEFORMAT,
                                       required=False)
    next_payment_date = forms.DateTimeField(input_formats=PAYPAL_DATEFORMAT,
                                            required=False)
    time_created = forms.DateTimeField(input_formats=PAYPAL_DATEFORMAT,
                                       required=False)

    def initialize(self, request):
        """Store the data we'll need to make the postback from the request
        object."""
        self.cleaned_data['query'] = getattr(request, request.method).urlencode()
        self.cleaned_data['ipaddress'] = request.META.get('REMOTE_ADDR', '')

    def clean_txn_id(self):
        '''check that this is a unique transaction id'''
        data = self.cleaned_data['txn_id']
        if PayPalIPN.objects.filter(txn_id=data).exists():
            self.set_flag('Transaction ID already exists')
        return data

    def clean_receiver_email(self):
        '''check that this notification was actually meant for us'''
        data = self.cleaned_data['receiver_email']
        if data != settings.PAYPAL_RECEIVER_EMAIL:
            self.set_flag('Invalid receiver email')
        return data

    def clean_payment_status(self):
        '''check that this a known payment status'''
        data = self.cleaned_data['payment_status']
        if data not in PayPalIPN.PAYMENT_STATUS_CHOICES:
            self.set_flag('Invalid payment status')
        return data

    def clean_query(self):
        '''postback to paypal to acknowledge they sent this notification'''
        data = self.cleaned_data['query']
        self.response = self._postback(data)
        if self.response != 'VERIFIED':
            self.set_flag('IPN not verified by PayPal')
        return data

    def clean_recurring_payment_id(self):
        '''check that we know this recurring payment profile'''
        if not PayPalUserSubscription.objects.filter(
                profileid=self.cleaned_data['recurring_payment_id']
        ):
            self.set_flag('No profile exists matching profileid')
        return self.cleaned_data['recurring_payment_id']

    def _postback(self, query):
        """Perform PayPal Postback validation."""
        return urllib2.urlopen(self.get_endpoint(),
                               "cmd=_notify-validate&%s" % query).read()

    def get_endpoint(self):
        '''returns which endpoint to use'''
        if settings.DEBUG:
            return settings.SANDBOX_POSTBACK_ENDPOINT
        return settings.POSTBACK_ENDPOINT

    def set_flag(self, info, code=None):
        """Sets a flag on the transaction and also sets a reason."""
        self.cleaned_data['flag'] = True
        if 'flag_info' in self.cleaned_data:
            self.cleaned_data['flag_info'] += info
        else:
            self.cleaned_data['flag_info'] = info
        if code is not None:
            self.cleaned_data['flag_code'] = code

    class Meta:
        model = PayPalIPN

