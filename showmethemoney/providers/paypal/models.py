from django.db import models
from showmethemoney.models import Transaction

class PaypalTransaction(Transaction):
    ipn = models.ForeignKey(ipn.models.PayPalIPN,
                            null=True, blank=True, editable=False)
