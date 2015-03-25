# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import pytest


@pytest.mark.onlydevel
def test_live(admin_browser):
    admin_browser.get('/admin/')
    admin_browser.get('/admin/custom_email_user/emailuser/')
    admin_browser.driver.find_elements_by_css_selector(
        'table#result_list tbody tr:nth-of-type(1)'
        ' th.field-email a')[0].click()
