# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
        ('showmethemoney', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayPalIPN',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business', models.CharField(help_text=b'Email where the money was sent.', max_length=127, blank=True)),
                ('receiver_email', models.EmailField(max_length=127, blank=True)),
                ('receiver_id', models.CharField(max_length=127, blank=True)),
                ('payment_status', models.CharField(max_length=9, blank=True)),
                ('payment_type', models.CharField(max_length=7, blank=True)),
                ('payment_date', models.DateTimeField(help_text=b'HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('txn_id', models.CharField(help_text=b'PayPal transaction ID.', max_length=19, verbose_name=b'Transaction ID', db_index=True, blank=True)),
                ('initial_payment_amount', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('initial_payment_txn_id', models.CharField(help_text=b'PayPal transaction ID.', max_length=19, verbose_name=b'Initial Transaction ID', blank=True)),
                ('txn_type', models.CharField(help_text=b'PayPal transaction type.', max_length=128, verbose_name=b'Transaction Type', blank=True)),
                ('mc_gross', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('mc_currency', models.CharField(default=b'USD', max_length=32, blank=True)),
                ('mc_fee', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('payment_gross', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('first_name', models.CharField(max_length=64, blank=True)),
                ('last_name', models.CharField(max_length=64, blank=True)),
                ('address_country', models.CharField(max_length=64, blank=True)),
                ('address_city', models.CharField(max_length=40, blank=True)),
                ('address_country_code', models.CharField(help_text=b'ISO 3166', max_length=64, blank=True)),
                ('address_name', models.CharField(max_length=128, blank=True)),
                ('address_state', models.CharField(max_length=40, blank=True)),
                ('address_status', models.CharField(max_length=11, blank=True)),
                ('address_street', models.CharField(max_length=200, blank=True)),
                ('address_zip', models.CharField(max_length=20, blank=True)),
                ('contact_phone', models.CharField(max_length=20, blank=True)),
                ('payer_email', models.CharField(max_length=127, blank=True)),
                ('payer_id', models.CharField(max_length=13, blank=True)),
                ('residence_country', models.CharField(max_length=2, blank=True)),
                ('amount', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('amount_per_cycle', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('next_payment_date', models.DateTimeField(help_text=b'HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('outstanding_balance', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('payment_cycle', models.CharField(max_length=32, blank=True)),
                ('period_type', models.CharField(max_length=32, blank=True)),
                ('product_name', models.CharField(max_length=128, blank=True)),
                ('product_type', models.CharField(max_length=128, blank=True)),
                ('profile_status', models.CharField(max_length=32, blank=True)),
                ('recurring_payment_id', models.CharField(max_length=128, blank=True)),
                ('rp_invoice_id', models.CharField(max_length=127, blank=True)),
                ('time_created', models.DateTimeField(help_text=b'HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('notify_version', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('charset', models.CharField(max_length=32, blank=True)),
                ('ipaddress', models.IPAddressField(null=True, blank=True)),
                ('flag', models.BooleanField(default=False)),
                ('flag_code', models.CharField(max_length=16, blank=True)),
                ('flag_info', models.TextField(blank=True)),
                ('query', models.TextField(blank=True)),
                ('response', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_view', models.CharField(max_length=6, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayPalTransaction',
            fields=[
                ('transaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='showmethemoney.Transaction')),
                ('ipn', models.ForeignKey(blank=True, editable=False, to='paypal.PayPalIPN', null=True)),
            ],
            bases=('showmethemoney.transaction',),
        ),
        migrations.CreateModel(
            name='PayPalUserSubscription',
            fields=[
                ('usersubscription_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='subscription.UserSubscription')),
                ('profileid', models.CharField(max_length=128)),
            ],
            bases=('subscription.usersubscription',),
        ),
    ]
