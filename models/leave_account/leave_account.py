# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("posted", "Posted")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveAccount(models.Model):
    _name = "leave.account"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    code = fields.Char(string="Code", readonly=True)

    _sql_constraints = [("code", "unique(code)", "Leave Account Code must be unique")]

    @api.multi
    def create(self, vals):
        vals["code"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(LeaveAccount, self).create(vals)
