# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CustomEmailUsersConfig(AppConfig):
    name = 'custom_email_user'
    verbose_name = _('users')