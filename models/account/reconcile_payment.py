# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
PROGRESS = [("draft", "Draft"), ("approved", "Approved")]


class ReconcilePayment(models.Model):
    _name = "reconcile.payment"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="qin.person", required=True)
    credit_ids = fields.One2many(comodel_name="reconcile.payment.item", inverse_name="credit_id")
    debit_ids = fields.One2many(comodel_name="reconcile.payment.item", inverse_name="debit_id")
