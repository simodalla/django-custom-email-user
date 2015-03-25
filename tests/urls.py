# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, patterns
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns(
    "",
    ("^admin/", include(admin.site.urls)),
)
