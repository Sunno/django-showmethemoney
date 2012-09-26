from django.utils.translation import ugettext_lazy as _

from subscription.models import Subscription
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

import floppyforms as forms

class SelectSubscriptionForm(forms.Form):
    subscription = forms.ModelChoiceField(queryset=Subscription.objects.all(),
                                          required=True,
                                          label='Select your subscription')
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'post'
        helper.form_class = 'form-container select-subscription-form'
        helper.layout = Layout(
            'subscription',
            Submit('_select', _(u'Continue with checkout'),
                   css_class='large-')
        )
        return helper
