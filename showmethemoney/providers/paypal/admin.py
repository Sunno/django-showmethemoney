from django.contrib import admin
from subscription.admin import UserSubscriptionAdmin, UserSubscriptionAdminForm
from models import PayPalUserSubscription


class PayPalUserSubscriptionAdminForm(UserSubscriptionAdminForm):
    class Meta:
        model = PayPalUserSubscription
        exclude = []


class PayPalUserSubscriptionAdmin(UserSubscriptionAdmin):
    form = PayPalUserSubscriptionAdminForm

    fieldsets = (
        (None, {'fields': ('user', 'subscription', 'expires', 'active',
                           'profileid', 'cancelled')}),
        ('Actions', {'fields': ('fix_group_membership', 'extend_subscription'),
                     'classes': ('collapse',)}),
        )

    search_fields = ('user__username', 'subscription__name')


admin.site.register(PayPalUserSubscription, PayPalUserSubscriptionAdmin)
