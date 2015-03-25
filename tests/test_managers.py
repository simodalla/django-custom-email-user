# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from datetime import datetime
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

import pytest

from django.test import TestCase, override_settings
from django.utils import timezone

from custom_email_user.models import EmailUser
from custom_email_user.managers import EmailUserManager

fake_now = datetime(2015, 9, 10)


@override_settings(USE_TZ=False)
class TestEmailUserManager(TestCase):

    def setUp(self):
        self.email = 'user@example.com'
        self.password = 'default'

    def test_private_create_user_without_email(self):
        """
        Test that EmailUser.objects._create_user without email raise an
        ValueError exception
        """
        with pytest.raises(ValueError) as exinfo:
            EmailUser.objects._create_user(None, None, False, False)
        self.assertIn('email must be set', str(exinfo.value))

    @patch.object(timezone, 'now', return_value=fake_now)
    def test_private_create_user_its_ok(self, mock_now):
        user = EmailUser.objects._create_user(self.email, self.password,
                                              True, False)
        self.assertTrue(isinstance(user, EmailUser))
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.date_joined, fake_now)
        self.assertEqual(user.last_login, fake_now)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(self.password))

    def test_private_create_user_with_wrong_email(self):
        with pytest.raises(ValueError) as exinfo:
            EmailUser.objects._create_user('wrong@example', None, False, False)
        self.assertIn('email must be a valid email', str(exinfo.value))

    @patch.object(EmailUserManager, '_create_user')
    def test_create_user_call_private_create_user_without_staff(
            self, mock_create_user):
        EmailUser.objects.create_user(self.email, self.password)
        mock_create_user.assert_called_once_with(
            self.email, self.password, False, False)

    @patch.object(EmailUserManager, '_create_user')
    def test_create_user_call_private_create_user_with_staff(
            self, mock_create_user):
        EmailUser.objects.create_user(self.email, self.password, True)
        mock_create_user.assert_called_once_with(
            self.email, self.password, True, False)

    @patch.object(EmailUserManager, '_create_user')
    def test_create_superuser_call_private_create_user(self, mock_create_user):
        EmailUser.objects.create_superuser(self.email, self.password)
        mock_create_user.assert_called_once_with(
            self.email, self.password, True, True)


