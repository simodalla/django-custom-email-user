# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core import mail
from django.utils.unittest import TestCase

from custom_email_user.models import EmailUser


class TestEmailUserModel(TestCase):

    def setUp(self):
        self.email = 'john.doe@example.com'
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.user = EmailUser(email=self.email)

    def test_get_fullname_no_first_name(self):
        """
        get_full_name return email field if first_name is None or empty
        """
        self.user.last_name = self.last_name
        self.assertEqual(self.user.get_full_name(), self.email)

    def test_get_fullname_no_last_name(self):
        """
        get_full_name return email field if last_name is None or empty
        """
        self.user.first_name = self.first_name
        self.assertEqual(self.user.get_full_name(), self.email)

    def test_get_fullname_with_last_and_first_name(self):
        """
        get_full_name return string 'first name last_name' if fields first_name
        and last_name are valorized
        """
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.assertEqual(self.user.get_full_name(),
                         '{} {}'.format(self.first_name, self.last_name))

    def test_str_method_return_get_full_name(self):
        """
        get_full_name is returned by __str__ method
        """
        self.assertEqual(self.user.__str__(), self.user.get_full_name())

    def test_get_short_name_return_first_name(self):
        """
        get_short_name is returned first_name if it'snt None
        """
        self.user.first_name = self.first_name
        self.assertEqual(self.user.get_short_name(), self.first_name)

    def test_get_short_name_return_last_name(self):
        """
        get_short_name is returned last_name if it'snt None and first_name is
        None
        """
        self.user.first_name = None
        self.user.last_name = self.last_name
        self.assertEqual(self.user.get_short_name(), self.last_name)

    def test_get_short_name_return_email(self):
        """
        get_short_name is returned email if first_name and last_name are both
        None
        """
        self.assertEqual(self.user.get_short_name(), self.email)

    def test_email_user_send_email_to_user(self):
        args = ('test subject', 'test message', 'from@example.com')
        self.user.email_user(*args)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, args[0])
        self.assertEqual(message.to, [self.user.email])
        self.assertEqual(message.from_email, args[2])
        self.assertEqual(message.body, args[1])

    def test_get_absolute_url(self):
        self.user.pk = 1
        self.assertEqual(self.user.get_absolute_url(),
                         '/admin/custom_email_user/emailuser/1/')
