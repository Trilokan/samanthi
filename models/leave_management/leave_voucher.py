# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Confirmed'),
                 ('cancelled', 'Cancelled')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveVoucher(models.Model):
    _name = "leave.voucher"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="qin.person", string="Person")
    credit_ids = fields.One2many(comodel_name="leave.voucher.item", inverse_name="credit_id")
    debit_ids = fields.One2many(comodel_name="leave.voucher.item", inverse_name="debit_id")
