# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.admin import AdminSite
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test import TestCase

from custom_email_user.models import EmailUser
from custom_email_user.forms import EmailUserCreationForm, EmailUserChangeForm
from custom_email_user.admin import EmailUserAdmin

from pyquery import PyQuery as pq


class TestAdminEmailUser(TestCase):
    def setUp(self):
        self.admin = EmailUser.objects.create_superuser(
            'admin@example.com', 'password')
        self.client.login(username=self.admin.email, password='password')

    def test_admin_add_form(self):
        response = self.client.get(reverse(admin_urlname(
            self.admin._meta, 'add')))
        admin_form = response.context['adminform']
        self.assertTrue(isinstance(admin_form.form, EmailUserCreationForm))

    def test_admin_change_form(self):
        response = self.client.get(reverse(admin_urlname(
            self.admin._meta, 'change'), args=(self.admin.pk,)))
        admin_form = response.context['adminform']
        self.assertTrue(isinstance(admin_form.form, EmailUserChangeForm))

    def test_ld_group_with_groups(self):
        emailuser_admin = EmailUserAdmin(EmailUser, AdminSite)
        groups = [Group.objects.create(name='group_{}'.format(i))
                  for i in range(1, 3)]
        self.admin.groups.add(*groups)
        result = pq(emailuser_admin.ld_groups(self.admin))
        self.assertSequenceEqual(
            [(a.text, a.attrib['href']) for a in result('a')],
            [(g.name, '/admin/auth/group/?id=%s' % g.pk) for g in groups])

    def test_ld_group_without_groups(self):
        emailuser_admin = EmailUserAdmin(EmailUser, AdminSite)
        result = emailuser_admin.ld_groups(self.admin)
        self.assertEqual(result, '')
