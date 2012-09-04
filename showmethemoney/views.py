from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from subscription.models import Subscription

class SubscriptionListView(ListView):
    model = Subscription
    context_object_name = 'subscription_list'
    template_name = 'showmethemoney/list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SubscriptionListView, self).dispatch(*args, **kwargs)
