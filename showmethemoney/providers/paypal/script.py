from showmethemoney.providers.paypal.views import _set_express_checkout_dict
from subscription.models import Subscription
from django.contrib.auth.models import User
print _set_express_checkout_dict(Subscription.objects.get(pk=1),
                                 User.objects.get(pk=1))
