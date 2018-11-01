# -*- coding: utf-8 -*-

from odoo import models, fields, api

PAYMENT_TYPE = [("customer_payment", "Customer Payment"), ("vendor_payment", "Vendor Payment")]


class Voucher(models.Model):
    _name = "hos.voucher"

    name = fields.Char(string="Name")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    payment_type = fields.Selection(selection=PAYMENT_TYPE, string="Payment Type")
    payment = fields.Float(strng="Payment")
    balance = fields.Float(strng="Balance")
    credit_ids = fields.One2many(comodel_name="voucher.line", inverse_name="credit_id", string="Credit")
    debit_ids = fields.One2many(comodel_name="voucher.line", inverse_name="debit_id", string="Debit")

    account_id = fields.Many2one(comodel_name="hos.account", string="Account")

    def reconciliation(self, rec, payment):
        items = []
        opening_balance = rec.total_amount - rec.opening_amount
        balance = opening_balance - rec.reconcile_amount

        if balance and payment:
            if payment > balance:
                rec.reconcile_amount = rec.reconcile_amount + balance
                payment = payment - balance
                items.append({"debit": balance})

            else:
                rec.reconcile_amount = rec.reconcile_amount + payment
                rec.reconcile = True
                items.append({"debit": payment})
                payment = 0

        print items

        return payment

    def trigger_reconcile(self):
        self.credit_ids.unlink()
        self.debit_ids.unlink()

        self.credit_ids = self.get_customer_credit_lines(self.account_id.id)
        self.debit_ids = self.get_customer_debit_lines(self.account_id.id)

        debits = self.debit_ids
        credits = self.credit_ids

        items = []

        data = {"credit": 0,
                "debit": 0,
                "reconcile_id": False,
                "reconcile_part_id": False,
                "account_id": self.account_id.id,
                "reference": self.name,
                "reconcile": False}

        # Debit
        for debit in debits:
            payment = (debit.total_amount - debit.opening_amount) - debit.reconcile_amount
            items.append({"credit": payment, "id": False})
            for rec in credits:

                opening_balance = rec.total_amount - rec.opening_amount
                balance = opening_balance - rec.reconcile_amount

                if balance and payment:
                    if payment > balance:
                        rec.reconcile_amount = rec.reconcile_amount + balance
                        payment = payment - balance
                        items.append({"debit": balance, "id": False})
                        debit.reconcile_amount = debit.reconcile_amount + balance

                    else:
                        rec.reconcile_amount = rec.reconcile_amount + payment
                        rec.reconcile = True
                        items.append({"debit": payment, "id": False})
                        debit.reconcile_amount = debit.reconcile_amount + payment
                        payment = 0

        # Credit
        payment = self.payment
        items.append({"credit": payment, "id": False})

        for rec in credits:
            opening_balance = rec.total_amount - rec.opening_amount
            balance = opening_balance - rec.reconcile_amount

            if balance and payment:
                if payment > balance:
                    rec.reconcile_amount = rec.reconcile_amount + balance
                    payment = payment - balance
                    items.append({"debit": balance, "id": False})

                else:
                    rec.reconcile_amount = rec.reconcile_amount + payment
                    rec.reconcile = True
                    items.append({"debit": payment, "id": False})
                    payment = 0

        journal_entry = self.env["journal.entries"].create({})
        journal_items = []

        for item in items:
            pass

    def trik(self):
        pass

    def get_customer_credit_lines(self, account_id):
        credit = []

        recs = self.env["journal.items"].search([("account_id", "=", account_id),
                                                 ("reconcile_id", "=", False),
                                                 ("credit", ">", 0)])

        for rec in recs:
            data = {"name": rec.name,
                    "total_amount": rec.credit,
                    "opening_amount": 0}

            if rec.reconcile_part_id:
                items = self.env["journal.items"].search([("reconcile_part_id", "=", rec.reconcile_part_id.id)])
                data["opening_amount"] = rec.credit - sum(items.mapped('debit'))

            credit.append((0, 0, data))

        return credit

    def get_customer_debit_lines(self, account_id):
        debit = []
        recs = self.env["journal.items"].search([("account_id", "=", account_id),
                                                 ("reconcile_id", "=", False),
                                                 ("debit", ">", 0)])

        for rec in recs:
            data = {"name": rec.name,
                    "total_amount": rec.debit,
                    "opening_amount": 0}

            if rec.reconcile_part_id:
                items = self.env["journal.items"].search([("reconcile_part_id", "=", rec.reconcile_part_id.id)])
                data["opening_amount"] = rec.debit - sum(items.mapped('credit'))

            debit.append((0, 0, data))

        return debit
