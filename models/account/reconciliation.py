# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QinReconciliation(models.Model):
    _name = "qin.reconciliation"

    name = fields.Char(string="Name", readonly=True)
    reconcile_ids = fields.One2many(comodel_name="journal.item", inverse_name="reconcile_id")
    part_reconcile_ids = fields.One2many(comodel_name="journal.item", inverse_name="part_reconcile_id")

    def get_balance(self, transaction):
        recs = self.part_reconcile_ids

        credit = 0
        debit = 0
        balance = 0
        for rec in recs:
            credit = credit + rec.credit
            debit = debit + rec.debit

        if transaction == "CREDIT":
            balance = credit - debit

        elif transaction == "DEBIT":
            balance = debit - credit

        if balance > 0:
            return balance
        else:
            return 0

