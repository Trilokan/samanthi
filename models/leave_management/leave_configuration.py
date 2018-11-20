# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Leave Configuration
class LeaveConfiguration(models.Model):
    _name = "leave.configuration"
    _inherit = "mail.thread"

    lop_id = fields.Many2one(comodel_name="leave.type", string="Loss Of Pay", required=True)
    account_id = fields.Many2one(comodel_name="leave.account", string="Leave Account", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id, readonly=True)
