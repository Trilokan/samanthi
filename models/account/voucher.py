# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

PAYMENT_TYPE = [("customer_payment", "Customer Payment"), ("vendor_payment", "Vendor Payment")]


class Voucher(models.Model):
    _name = "hos.voucher"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    payment_type = fields.Selection(selection=PAYMENT_TYPE, string="Payment Type", required=True)
    payment = fields.Float(strng="Payment", default=0, required=True)
    balance = fields.Float(strng="Balance", default=0, required=True)
    credit_ids = fields.One2many(comodel_name="voucher.line", inverse_name="credit_id", string="Credit")
    debit_ids = fields.One2many(comodel_name="voucher.line", inverse_name="debit_id", string="Debit")
    payment_account_id = fields.Many2one(comodel_name="hos.account", string="Payment Account")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    dummy_ids = fields.One2many(comodel_name="voucher.dummy", inverse_name="voucher_id", string="Dummy")
    entry_id = fields.Many2one(comodel_name="journal.entries", string="Journal Entries")

    def reconciliation(self, credits, payment, item_id=False, is_payment=True):
        for rec in credits:
            opening_balance = rec.total_amount - rec.opening_amount
            balance = opening_balance - rec.reconcile_amount

            if balance and payment:
                if not rec.reconcile_part_id:
                    reconcile_part_id = self.env["hos.reconcile"].create({})
                    rec.reconcile_part_id = reconcile_part_id.id

                if payment > balance:
                    rec.reconcile_amount = rec.reconcile_amount + balance
                    payment = payment - balance
                    data = {"debit": balance,
                            "item_id": item_id,
                            "reconcile_part_id": rec.reconcile_part_id.id,
                            "account_id": self.account_id.id,
                            "is_payment": is_payment,
                            "voucher_id": self.id}

                    self.env["voucher.dummy"].create(data)

                else:
                    rec.reconcile_amount = rec.reconcile_amount + payment
                    rec.reconcile = True
                    data = {"debit": payment,
                            "item_id": item_id,
                            "reconcile_part_id": rec.reconcile_part_id.id,
                            "account_id": self.account_id.id,
                            "is_payment": is_payment,
                            "voucher_id": self.id}

                    self.env["voucher.dummy"].create(data)
                    payment = 0

        return payment

    def debit_split(self, recs):
        item = recs[0].item_id
        journal_item_data = item.copy_data()
        for line in recs:
            new_fling = journal_item_data[0]
            new_fling["debit"] = line.debit
            new_fling["reconcile_part_id"] = line.reconcile_part_id.id
            self.env["journal.items"].create(new_fling)

        item.unlink()

    def update_payment_journal(self):
        recs = self.debit_ids

        for rec in recs:
            item = self.env["voucher.dummy"].search([("item_id", "=", rec.item_id.id)])

            if len(item) == 1:
                item.item_id.reconcile_part_id = item.reconcile_part_id.id
            elif len(item) > 1:
                self.debit_split(item)

        recs = self.credit_ids
        for rec in recs:
            rec.item_id.reconcile_part_id = rec.reconcile_part_id.id

    def payment_reconcile(self):
        credits = self.credit_ids
        payment = self.payment

        data = {"credit": payment,
                "account_id": self.payment_account_id.id,
                "is_payment": True,
                "voucher_id": self.id}

        self.env["voucher.dummy"].create(data)

        reconcile = self.reconciliation(credits, payment)
        if reconcile:
            data = {"debit": reconcile,
                    "account_id": self.account_id.id,
                    "is_payment": True,
                    "voucher_id": self.id}

            self.env["voucher.dummy"].create(data)

    def debit_amount_reconcile(self):
        debits = self.debit_ids
        credits = self.credit_ids

        for debit in debits:
            payment = (debit.total_amount - debit.opening_amount) - debit.reconcile_amount

            reconcile = self.reconciliation(credits, payment, debit.item_id.id, False)

            if reconcile != payment:
                data = {"debit": reconcile,
                        "item_id": debit.item_id.id,
                        "account_id": self.account_id.id,
                        "is_payment": False,
                        "voucher_id": self.id}

                self.env["voucher.dummy"].create(data)

            debit.reconcile_amount = reconcile

    def generate_payment_journals(self):
        recs = self.env["voucher.dummy"].search([("is_payment", "=", True), ("voucher_id", "=", self.id)])

        item = []
        for rec in recs:
            data = {"description": "Payment",
                    "account_id": rec.account_id.id,
                    "person_id": self.person_id.id,
                    "credit": rec.credit,
                    "debit": rec.debit,
                    "reconcile_part_id": rec.reconcile_part_id.id}

            item.append((0, 0, data))

        self.env["journal.entries"].create({"item_ids": item})

    def trigger_reconcile(self):
        # Unlink all existing data
        self.credit_ids.unlink()
        self.debit_ids.unlink()
        self.dummy_ids.unlink()

        # Set credit and debit lines
        self.credit_ids = self.get_customer_credit_lines(self.account_id.id)
        self.debit_ids = self.get_customer_debit_lines(self.account_id.id)

        # Payment reconciliation
        self.debit_amount_reconcile()
        self.payment_reconcile()

    def trigger_confirmed(self):
        self.trigger_reconcile()
        self.generate_payment_journals()
        self.update_payment_journal()

    def get_customer_credit_lines(self, account_id):
        credit = []

        recs = self.env["journal.items"].search([("account_id", "=", account_id),
                                                 ("reconcile_id", "=", False),
                                                 ("credit", ">", 0)])

        for rec in recs:
            data = {"name": rec.name,
                    "description": rec.description,
                    "account_id": rec.account_id.id,
                    "total_amount": rec.credit,
                    "item_id": rec.id}

            if rec.reconcile_part_id:
                items = self.env["journal.items"].search([("reconcile_part_id", "=", rec.reconcile_part_id.id)])
                data["opening_amount"] = sum(items.mapped('debit'))
                data["reconcile_part_id"] = rec.reconcile_part_id.id,

            credit.append((0, 0, data))

        return credit

    def get_customer_debit_lines(self, account_id):
        debit = []
        recs = self.env["journal.items"].search([("account_id", "=", account_id),
                                                 ("reconcile_id", "=", False),
                                                 ("reconcile_part_id", "=", False),
                                                 ("debit", ">", 0)])

        for rec in recs:
            data = {"name": rec.name,
                    "description": rec.description,
                    "account_id": rec.account_id.id,
                    "total_amount": rec.debit,
                    "reconcile_part_id": rec.reconcile_part_id.id,
                    "item_id": rec.id}

            debit.append((0, 0, data))

        return debit
