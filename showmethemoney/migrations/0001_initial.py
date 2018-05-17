# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('event', models.CharField(max_length=100, editable=False)),
                ('amount', models.DecimalField(null=True, editable=False, max_digits=64, decimal_places=2, blank=True)),
                ('comment', models.TextField(default=b'', blank=True)),
                ('subscription', models.ForeignKey(blank=True, editable=False, to='subscription.Subscription', null=True)),
                ('user', models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
    ]
