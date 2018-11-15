# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveVoucherDummy(models.Model):
    _name = "leave.voucher.dummy"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    account_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    description = fields.Text(string="Description")
    credit = fields.Float(string="Credit", default=0, required=True)
    debit = fields.Float(string="Debit", default=0, required=True)
    part_reconcile_id = fields.Many2one(comodel_name="leave.reconcile", string="Partial Reconcile", required=True)
    voucher_id = fields.Many2one(comodel_name="leave.voucher", string="Leave Voucher", required=True)


