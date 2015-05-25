# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_email_user', '0002_auto_20150525_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailuser',
            name='username_for_conversion_1',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='emailuser',
            name='username_for_conversion_2',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]
