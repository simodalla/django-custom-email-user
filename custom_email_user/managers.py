# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.mail import mail_admins
from django.core.validators import validate_email
from django.template import loader, Context
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _


class EmailUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError(_('The given email must be set'))
        try:
            email = self.normalize_email(email)
            validate_email(email)
        except ValidationError:
            raise ValueError(_('The given email must be a valid email'))

        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, is_staff=False,
                    **extra_fields):
        return self._create_user(email, password, is_staff, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

    # def copy_fields(self, dest_user, source_user, fields=None,
    #                 dest_update=True):
    #     """
    #     Update fields from list param 'fields' to 'dest_user' User from
    #     'source_user' User.
    #     """
    #     fields = fields or []
    #     changed = False
    #     for field in fields:
    #         social_field = getattr(source_user, field)
    #         if not (getattr(dest_user, field) == social_field):
    #             setattr(dest_user, field, social_field)
    #             changed = True
    #     if changed and dest_update:
    #         dest_user.save()
    #     return changed

    # def set_fields_from_authorized(self, dest_user, authorized_user,
    #                                fields=None):
    #     fields = fields or ['is_staff', 'is_superuser']
    #     for field in fields:
    #         setattr(dest_user, field, getattr(authorized_user, field, False))
    #
    # def _email_for_sociallogin(self, subject, template, context=None):
    #     context = context or {}
    #     message = loader.get_template(template).render(Context(context))
    #     mail_admins(subject,
    #                 strip_tags(message).lstrip('\n'),
    #                 fail_silently=True,
    #                 html_message=message)

    # def email_new_sociallogin(self, request, user):
    #     from django.core.urlresolvers import reverse
    #     from django.contrib.admin.templatetags.admin_urls import admin_urlname
    #     context = {'email': user.email,
    #                'user_url': request.build_absolute_uri(
    #                    reverse(admin_urlname(user._meta, 'changelist')))
    #                            + '?email={}'.format(user.email)}
    #     subject = 'Nuovo socialaccount di {}'.format(user.email)
    #     return self._email_for_sociallogin(
    #         subject, "custom_email_user/email/new_sociallogin.html", context)

    # def email_link_sociallogin(self, request, user):
    #     context = {'email': user.email,
    #                'user_url': request.build_absolute_uri(
    #                    user.get_absolute_url())}
    #     subject = 'Collegamento socialaccount di {}'.format(user.email)
    #     return self._email_for_sociallogin(
    #         subject, "custom_email_user/email/link_sociallogin.html", context)
