# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
PROGRESS = [("draft", "Draft"), ("approved", "Approved")]


class PaymentReconcile(models.Model):
    _name = "payment.reconcile"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="qin.person", required=True)
    credit_ids = fields.One2many(comodel_name="payment.reconcile.item", inverse_name="credit_id")
    debit_ids = fields.One2many(comodel_name="payment.reconcile.item", inverse_name="debit_id")

    def _get_transaction_ids(self):
        credit_recs = self.env["journal.item"].get_credit_balance(self.person_id, self.id)
        debit_recs = self.env["journal.item"].get_debit_balance(self.person_id)

        for rec in credit_recs:
            self.env["payment.reconcile.item"].create(rec)

        for rec in debit_recs:
            self.env["payment.reconcile.item"].create(rec)

    def trigger_reconcile(self):
        pass

