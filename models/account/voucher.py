# -*- coding: utf-8 -*-

from odoo import models, fields, api

PAYMENT_TYPE = [("customer_payment", "Customer Payment"), ("vendor_payment", "Vendor Payment")]


class Voucher(models.Model):
    _name = "hos.voucher"

    name = fields.Char(string="Name")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    payment_type = fields.Selection(selection=PAYMENT_TYPE, string="Payment Type")
    payment = fields.Float(strng="Payment")
    balance = fields.Float(string="Balance")
    credit_ids = fields.One2many(comodel_name="voucher.line", inverse_name="credit_id", string="Credit")
    debit_ids = fields.One2many(comodel_name="voucher.line", inverse_name="debit_id", string="Debit")

    account_id = fields.Many2one(comodel_name="hos.account", string="Account")

    @api.multi
    def get_items(self):
        self.credit_ids.unlink()
        self.debit_ids.unlink()

        account_id = self.person_id.payable_id or self.person_id.receivable_id

        self.credit_ids, self.debit_ids = self.env["journal.items"].get_items(account_id, self.id)

    @api.multi
    def trigger_reconciliation(self):
        if self.person_id and self.payment_type:
            self.get_items()

        # self.reco(self.debit_ids, self.amount)
        #
        # for rec in self.credit_ids:
        #     self.reco(self.debit_ids, rec.opening_amount)

    def reco(self, obj, amount):
        items = []

        for rec in obj:
            reconcile = rec.opening_amount - rec.reconcile_amount
            if amount and reconcile:
                if amount > reconcile:
                    rec.reconcile_amount = rec.reconcile_amount + reconcile
                else:
                    rec.reconcile_amount = rec.reconcile_amount + amount




