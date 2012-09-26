from django.dispatch import Signal

pre_set_express_checkout = Signal()
post_set_express_checkout = Signal()

pre_redirect_to_paypal = Signal()
post_redirect_to_paypal = Signal()

pre_get_express_checkout_details = Signal()
post_get_express_checkout_details = Signal()

pre_do_express_checkout_payment = Signal()
post_do_express_checkout_payment = Signal()

pre_create_recurring_profile = Signal()
post_create_recurring_profile = Signal()

#payment_was_successful = Signal()
payment_was_flagged = Signal()
recurring_create = Signal()
recurring_expired = Signal()
recurring_payment = Signal()
recurring_skipped = Signal()
recurring_cancelled = Signal()
