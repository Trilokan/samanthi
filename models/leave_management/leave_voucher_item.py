# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Confirmed'),
                 ('cancelled', 'Cancelled')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveVoucherItem(models.Model):
    _name = "leave.voucher.item"

    select_rec = fields.Boolean(string="Select")
    date = fields.Date(string="Date")
    person_id = fields.Many2one(comodel_name="qin.person", string="Person")
    leave_type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    description = fields.Text(string="Description")
    reference = fields.Text(string="Reference")
    total_days = fields.Float(string="Total", default=0.0)
    available_days = fields.Float(string="Available", default=0.0)
    reconcile_days = fields.Float(string="Reconcile", default=0.0)
    balance_days = fields.Float(string="Balance", default=0.0)
    credit_id = fields.Many2one(comodel_name="leave.voucher", string="Leave Credit")
    debit_id = fields.Many2one(comodel_name="leave.voucher", string="Leave Debit")
