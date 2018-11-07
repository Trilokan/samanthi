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
    payment_account_id = fields.Many2one(comodel_name="hos.account", string="Payment Account")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    dummy_ids = fields.One2many(comodel_name="voucher.dummy", inverse_name="voucher_id", string="Dummy")

    def gtyu(self, credits, payment, item_id=False):
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
                    data = {"amount": balance,
                            "item_id": item_id,
                            "reconcile_part_id": rec.reconcile_part_id.id,
                            "account_id": self.account_id.id,
                            "voucher_id": self.id}

                    self.env["voucher.dummy"].create(data)

                else:
                    rec.reconcile_amount = rec.reconcile_amount + payment
                    rec.reconcile = True
                    data = {"amount": payment,
                            "item_id": item_id,
                            "reconcile_part_id": rec.reconcile_part_id.id,
                            "account_id": self.account_id.id,
                            "voucher_id": self.id}

                    self.env["voucher.dummy"].create(data)
                    payment = 0


        return payment

    def payment_reconcile(self):
        credits = self.credit_ids
        payment = self.payment

        reconcile = self.gtyu(credits, payment)
        if reconcile:
            data = {"amount": reconcile,
                    "account_id": self.account_id.id,
                    "voucher_id": self.id}

            self.env["voucher.dummy"].create(data)

    def reconcile_debit_amount(self):
        debits = self.debit_ids
        credits = self.credit_ids

        for debit in debits:
            payment = (debit.total_amount - debit.opening_amount) - debit.reconcile_amount

            reconcile = self.gtyu(credits, payment, debit.item_id.id)

            if reconcile != payment:
                data = {"amount": reconcile,
                        "item_id": debit.item_id.id,
                        "account_id": self.account_id.id,
                        "voucher_id": self.id}

                self.env["voucher.dummy"].create(data)

            debit.reconcile_amount = reconcile

    def get_item_id(self):
        recs = self.env["voucher.dummy"].search([("item_id", "!=", False)])
        item_ids = []
        duplicate_ids = []
        real_ids = []

        for rec in recs:
            if rec.item_id in item_ids:
                duplicate_ids.append(rec.item_id)
            item_ids.append(rec.item_id)

        for rec in recs:
            if rec.item_id not in duplicate_ids:
                real_ids.append(rec.item_id)

        return real_ids, duplicate_ids

    def generate_payment_journals(self):
        recs = self.env["voucher.dummy"].search([("item_id", "=", False)])

        item = []
        for rec in recs:
            data = {"debit": rec.amount,
                    "account_id": self.account_id.id,
                    "reconcile_part_id": rec.reconcile_part_id.id}

            item.append((0, 0, data))

        data = {"credit": self.payment,
                "account_id": self.payment_account_id.id}

        item.append((0, 0, data))

        self.env["journal.entries"].create({"item_ids": item})

    def debit_split(self, recs):
        for rec in recs:
            records = self.env["voucher.dummy"].search([("item_id", "=", rec.id),
                                                        ("voucher_id", "=", self.id)])

            journal_item_data = rec.copy_data()

            for line in records:
                new_fling = journal_item_data[0]
                new_fling["debit"] = line.amount
                new_fling["reconcile_part_id"] = line.reconcile_part_id.id
                self.env["journal.items"].create(new_fling)

            rec.unlink()

    def update_debit_reconcile(self, recs):
        for rec in recs:
            dummy = self.env["voucher.dummy"].search([("item_id", "=", rec.id)])
            rec.reconcile_part_id = dummy.reconcile_part_id.id

    def update_credit_reconcile(self):
        credits = self.credit_ids
        for rec in credits:
            rec.item_id.reconcile_part_id = rec.reconcile_part_id.id
            self.env["hos.reconcile"].check_reconciliation(rec.reconcile_part_id.id)

    def trigger_reconcile(self):
        # Unlink all existing data
        self.credit_ids.unlink()
        self.debit_ids.unlink()
        self.dummy_ids.unlink()

        # Set credit and debit lines
        self.credit_ids = self.get_customer_credit_lines(self.account_id.id)
        self.debit_ids = self.get_customer_debit_lines(self.account_id.id)

        # Payment reconciliation
        self.reconcile_debit_amount()
        self.payment_reconcile()

    def trigger_confirmed(self):
        self.trigger_reconcile()
        self.generate_payment_journals()
        real_ids, duplicate_ids = self.get_item_id()

        self.debit_split(duplicate_ids)
        self.update_debit_reconcile(real_ids)
        self.update_credit_reconcile()

    def trigger_cancel(self):
        pass

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
