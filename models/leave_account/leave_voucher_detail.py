# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveVoucherDetail(models.Model):
    _name = "leave.voucher.detail"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    account_id = fields.Many2one(comodel_name="leave.account", string="Account")
    type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    description = fields.Text(string="Description")
    available = fields.Float(string="Available", default=0)
    opening = fields.Float(string="Opening", default=0)
    reconcile = fields.Float(string="Reconcile", default=0)
    item_id = fields.Many2one(comodel_name="leave.journal.item", string="Journal Item")
    part_reconcile_id = fields.Many2one(comodel_name="leave.reconcile", string="Partial Reconcile")
    voucher_id = fields.Many2one(comodel_name="leave.voucher", string="Leave Voucher")

