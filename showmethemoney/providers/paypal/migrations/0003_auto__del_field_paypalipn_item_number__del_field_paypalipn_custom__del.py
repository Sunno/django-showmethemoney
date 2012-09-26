# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'PayPalIPN.item_number'
        db.delete_column('paypal_paypalipn', 'item_number')

        # Deleting field 'PayPalIPN.custom'
        db.delete_column('paypal_paypalipn', 'custom')

        # Deleting field 'PayPalIPN.item_name'
        db.delete_column('paypal_paypalipn', 'item_name')

        # Adding field 'PayPalIPN.business'
        db.add_column('paypal_paypalipn', 'business',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=127, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.receiver_id'
        db.add_column('paypal_paypalipn', 'receiver_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=127, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.payment_type'
        db.add_column('paypal_paypalipn', 'payment_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=7, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.payment_date'
        db.add_column('paypal_paypalipn', 'payment_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.initial_payment_txn_id'
        db.add_column('paypal_paypalipn', 'initial_payment_txn_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=19, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.mc_fee'
        db.add_column('paypal_paypalipn', 'mc_fee',
                      self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=64, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.payment_gross'
        db.add_column('paypal_paypalipn', 'payment_gross',
                      self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=64, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.first_name'
        db.add_column('paypal_paypalipn', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.last_name'
        db.add_column('paypal_paypalipn', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.address_country'
        db.add_column('paypal_paypalipn', 'address_country',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.address_city'
        db.add_column('paypal_paypalipn', 'address_city',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.address_country_code'
        db.add_column('paypal_paypalipn', 'address_country_code',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.address_name'
        db.add_column('paypal_paypalipn', 'address_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.address_state'
        db.add_column('paypal_paypalipn', 'address_state',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.address_status'
        db.add_column('paypal_paypalipn', 'address_status',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=11, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.address_street'
        db.add_column('paypal_paypalipn', 'address_street',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.address_zip'
        db.add_column('paypal_paypalipn', 'address_zip',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.contact_phone'
        db.add_column('paypal_paypalipn', 'contact_phone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.payer_id'
        db.add_column('paypal_paypalipn', 'payer_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=13, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.residence_country'
        db.add_column('paypal_paypalipn', 'residence_country',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.notify_version'
        db.add_column('paypal_paypalipn', 'notify_version',
                      self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=64, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.charset'
        db.add_column('paypal_paypalipn', 'charset',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'PayPalIPN.item_number'
        db.add_column('paypal_paypalipn', 'item_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=127, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.custom'
        db.add_column('paypal_paypalipn', 'custom',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'PayPalIPN.item_name'
        db.add_column('paypal_paypalipn', 'item_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=127, blank=True),
                      keep_default=False)

        # Deleting field 'PayPalIPN.business'
        db.delete_column('paypal_paypalipn', 'business')

        # Deleting field 'PayPalIPN.receiver_id'
        db.delete_column('paypal_paypalipn', 'receiver_id')

        # Deleting field 'PayPalIPN.payment_type'
        db.delete_column('paypal_paypalipn', 'payment_type')

        # Deleting field 'PayPalIPN.payment_date'
        db.delete_column('paypal_paypalipn', 'payment_date')

        # Deleting field 'PayPalIPN.initial_payment_txn_id'
        db.delete_column('paypal_paypalipn', 'initial_payment_txn_id')

        # Deleting field 'PayPalIPN.mc_fee'
        db.delete_column('paypal_paypalipn', 'mc_fee')

        # Deleting field 'PayPalIPN.payment_gross'
        db.delete_column('paypal_paypalipn', 'payment_gross')

        # Deleting field 'PayPalIPN.first_name'
        db.delete_column('paypal_paypalipn', 'first_name')

        # Deleting field 'PayPalIPN.last_name'
        db.delete_column('paypal_paypalipn', 'last_name')

        # Deleting field 'PayPalIPN.address_country'
        db.delete_column('paypal_paypalipn', 'address_country')

        # Deleting field 'PayPalIPN.address_city'
        db.delete_column('paypal_paypalipn', 'address_city')

        # Deleting field 'PayPalIPN.address_country_code'
        db.delete_column('paypal_paypalipn', 'address_country_code')

        # Deleting field 'PayPalIPN.address_name'
        db.delete_column('paypal_paypalipn', 'address_name')

        # Deleting field 'PayPalIPN.address_state'
        db.delete_column('paypal_paypalipn', 'address_state')

        # Deleting field 'PayPalIPN.address_status'
        db.delete_column('paypal_paypalipn', 'address_status')

        # Deleting field 'PayPalIPN.address_street'
        db.delete_column('paypal_paypalipn', 'address_street')

        # Deleting field 'PayPalIPN.address_zip'
        db.delete_column('paypal_paypalipn', 'address_zip')

        # Deleting field 'PayPalIPN.contact_phone'
        db.delete_column('paypal_paypalipn', 'contact_phone')

        # Deleting field 'PayPalIPN.payer_id'
        db.delete_column('paypal_paypalipn', 'payer_id')

        # Deleting field 'PayPalIPN.residence_country'
        db.delete_column('paypal_paypalipn', 'residence_country')

        # Deleting field 'PayPalIPN.notify_version'
        db.delete_column('paypal_paypalipn', 'notify_version')

        # Deleting field 'PayPalIPN.charset'
        db.delete_column('paypal_paypalipn', 'charset')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'relationships': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'symmetrical': 'False', 'through': "orm['relationships.Relationship']", 'to': "orm['auth.User']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'paypal.paypalipn': {
            'Meta': {'object_name': 'PayPalIPN'},
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'address_country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'address_country_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'address_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'address_state': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'address_status': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'address_street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'address_zip': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '64', 'decimal_places': '2', 'blank': 'True'}),
            'amount_per_cycle': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '64', 'decimal_places': '2', 'blank': 'True'}),
            'business': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'charset': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flag_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'flag_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'from_view': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_payment_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '64', 'decimal_places': '2', 'blank': 'True'}),
            'initial_payment_txn_id': ('django.db.models.fields.CharField', [], {'max_length': '19', 'blank': 'True'}),
            'ipaddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'mc_currency': ('django.db.models.fields.CharField', [], {'default': "'USD'", 'max_length': '32', 'blank': 'True'}),
            'mc_fee': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '64', 'decimal_places': '2', 'blank': 'True'}),
            'mc_gross': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '64', 'decimal_places': '2', 'blank': 'True'}),
            'next_payment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'notify_version': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '64', 'decimal_places': '2', 'blank': 'True'}),
            'outstanding_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '64', 'decimal_places': '2', 'blank': 'True'}),
            'payer_email': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'payer_id': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'payment_cycle': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'payment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'payment_gross': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '64', 'decimal_places': '2', 'blank': 'True'}),
            'payment_status': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'period_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'product_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'profile_status': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'receiver_email': ('django.db.models.fields.EmailField', [], {'max_length': '127', 'blank': 'True'}),
            'receiver_id': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'recurring_payment_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'residence_country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rp_invoice_id': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'txn_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '19', 'blank': 'True'}),
            'txn_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'paypal.paypaltransaction': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'PayPalTransaction', '_ormbases': ['showmethemoney.Transaction']},
            'ipn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paypal.PayPalIPN']", 'null': 'True', 'blank': 'True'}),
            'transaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['showmethemoney.Transaction']", 'unique': 'True', 'primary_key': 'True'})
        },
        'paypal.paypalusersubscription': {
            'Meta': {'object_name': 'PayPalUserSubscription', '_ormbases': ['subscription.UserSubscription']},
            'profileid': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'usersubscription_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['subscription.UserSubscription']", 'unique': 'True', 'primary_key': 'True'})
        },
        'relationships.relationship': {
            'Meta': {'ordering': "('created',)", 'unique_together': "(('from_user', 'to_user', 'status', 'site'),)", 'object_name': 'Relationship'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_users'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'relationships'", 'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relationships.RelationshipStatus']"}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_users'", 'to': "orm['auth.User']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'null': 'True', 'blank': 'True'})
        },
        'relationships.relationshipstatus': {
            'Meta': {'ordering': "('name',)", 'object_name': 'RelationshipStatus'},
            'from_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'symmetrical_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'to_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'showmethemoney.transaction': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '64', 'decimal_places': '2', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['subscription.Subscription']", 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'subscription.subscription': {
            'Meta': {'ordering': "('price', '-recurrence_period')", 'object_name': 'Subscription'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '64', 'decimal_places': '2'}),
            'recurrence_period': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recurrence_unit': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'trial_period': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trial_unit': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        'subscription.usersubscription': {
            'Meta': {'unique_together': "(('user', 'subscription'),)", 'object_name': 'UserSubscription'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['subscription.Subscription']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['paypal']