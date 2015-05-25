# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_email_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailuser',
            name='id_for_conversion_1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='emailuser',
            name='id_for_conversion_2',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
