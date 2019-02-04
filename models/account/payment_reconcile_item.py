# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
PROGRESS = [("draft", "Draft"), ("approved", "Approved")]


class PaymentReconcileItem(models.Model):
    _name = "payment.reconcile.item"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    invoice_id = fields.Many2one(comodel_name="qin.invoice", string="Invoice")
    description = fields.Text(string="Description")
    amount = fields.Float(string="Amount")
    balance = fields.Float(string="Balance")
    select_rec = fields.Boolean(string="Select")
    credit_id = fields.Many2one(comodel_name="payment.reconcile", string="Credit")
    debit_id = fields.Many2one(comodel_name="payment.reconcile", string="Debit")

