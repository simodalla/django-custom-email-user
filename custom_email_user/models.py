# -*- coding: utf-8 -*-

from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .managers import EmailUserManager


@python_2_unicode_compatible
class EmailUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    id_for_conversion_1 = models.IntegerField(blank=True, null=True)
    username_for_conversion_1 = models.CharField(max_length=254, blank=True)
    id_for_conversion_2 = models.IntegerField(blank=True, null=True)
    username_for_conversion_2 = models.CharField(max_length=254, blank=True)

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return reverse(admin_urlname(self._meta, 'change'), args=(self.pk,))

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = self.email
        if self.first_name and self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.email

    def get_short_name(self):
        """Returns the short name for the user."""
        if self.first_name:
            return self.first_name.strip()
        elif self.last_name:
            return self.last_name.strip()
        return self.email

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        return send_mail(subject, message, from_email, [self.email])

    @staticmethod
    def autocomplete_search_fields():
        """
        Grapelli autocomplete method.
        """
        return ['id__iexact', 'email__icontains']
