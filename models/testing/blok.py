# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import werkzeug

from odoo import http
from odoo.http import request


class LinkTracker(http.Controller):
    @http.route('/ram', type='http', auth='none', website=True)
    def full_url_redirect(self):
        request.session

