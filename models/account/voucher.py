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

    def payment_reconcile(self):
        credits = self.credit_ids
        payment = self.payment

        for rec in credits:
            opening_balance = rec.total_amount - rec.opening_amount
            balance = opening_balance - rec.reconcile_amount

            if balance and payment:
                if payment > balance:
                    rec.reconcile_amount = rec.reconcile_amount + balance
                    payment = payment - balance
                    data = {"amount": balance,
                            "reconcile_part_id": rec.reconcile_part_id,
                            "account_id": self.payment_account_id.id,
                            "voucher_id": self.id}

                    self.env["voucher.dummy"].create(data)

                else:
                    rec.reconcile_amount = rec.reconcile_amount + payment
                    rec.reconcile = True
                    data = {"amount": payment,
                            "reconcile_part_id": rec.reconcile_part_id,
                            "account_id": self.payment_account_id.id,
                            "voucher_id": self.id}

                    self.env["voucher.dummy"].create(data)
                    payment = 0

        if payment:
            data = {"amount": payment,
                    "reconcile_part_id": False,
                    "account_id": self.account_id.id,
                    "voucher_id": self.id}

            self.env["voucher.dummy"].create(data)

    def reconcile_debit_amount(self):
        debits = self.debit_ids
        credits = self.credit_ids

        for debit in debits:
            payment = (debit.total_amount - debit.opening_amount) - debit.reconcile_amount

            for rec in credits:
                opening_balance = rec.total_amount - rec.opening_amount
                balance = opening_balance - rec.reconcile_amount

                if balance and payment:
                    if not rec.reconcile_part_id:
                        reconcile_part_id = self.env["hos.reconciliation"].create({})
                        rec.reconcile_part_id = reconcile_part_id.id

                    if payment > balance:
                        rec.reconcile_amount = rec.reconcile_amount + balance
                        payment = payment - balance
                        data = {"amount": balance,
                                "item_id": debit.item_id.id,
                                "reconcile_part_id": rec.reconcile_part_id,
                                "account_id": debit.account_id.id,
                                "voucher_id": self.id}

                        self.env["voucher.dummy"].create(data)

                    else:
                        rec.reconcile_amount = rec.reconcile_amount + payment
                        rec.reconcile = True
                        data = {"amount": payment,
                                "item_id": debit.item_id.id,
                                "reconcile_part_id": rec.reconcile_part_id,
                                "account_id": debit.account_id.id,
                                "voucher_id": self.id}

                        self.env["voucher.dummy"].create(data)
                        payment = 0

            if payment:
                data = {"amount": payment,
                        "item_id": debit.id,
                        "reconcile_part_id": False,
                        "account_id": debit.account_id.id,
                        "voucher_id": self.id}

                self.env["voucher.dummy"].create(data)

    def get_item_id(self):
        recs = self.dummy_ids
        item_ids = []
        duplicate_ids = []

        for rec in recs:
            if rec.item_id in item_ids:
                duplicate_ids.append(rec.item_id)
            item_ids.append(rec.item_id)

        return duplicate_ids

    def generate_payment_journals(self):
        item_ids = self.dummy_ids

        item =[]
        for rec in item_ids:
            data = {"debit": rec.amount,
                    "account_id": self.account_id.id,
                    "reconcile_part_id": rec.reconcile_part_id.id}

            item.append((0, 0, data))

        data = {"credit": self.payment,
                "account_id": self.payment_account_id.id}

        item.append((0, 0, data))

        self.env["journal.items"].create({"item_ids" : item})

    def debit_split(self, item_ids):
        for rec in item_ids:
            records = self.env["voucher.dummy"].search([("item_id", "=", rec.id),
                                                        ("voucher_id", "=", self.id)])

            data = []

            journal_item_data = rec.copy_data()

            for line in records:
                new_fling = journal_item_data[0]
                new_fling["debit"] = line.amount
                new_fling["reconcile_part_id"] = line.reconcile_part_id.id
                self.env["journal.items"].create(new_fling)

            rec.active = False

    def update_debit_reconcile(self):
        item_ids  =self.dummy_ids

        for rec in item_ids:
            if rec.item_id:
                rec.item_id.reconcile_part_id = rec.reconcile_part_id.id

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

        # Debit split
        item_ids = self.get_item_id()
        self.debit_split(item_ids)
        item_ids.unlink()

        self.update_debit_reconcile()




    def get_customer_credit_lines(self, account_id):
        credit = []

        recs = self.env["journal.items"].search([("account_id", "=", account_id),
                                                 ("reconcile_id", "=", False),
                                                 ("credit", ">", 0)])

        for rec in recs:
            data = {"name": rec.name,
                    "total_amount": rec.credit,
                    "account_id": rec.account_id.id,
                    "item_id": rec.id}

            if rec.reconcile_part_id:
                items = self.env["journal.items"].search(["|",
                                                          ("reconcile_part_id", "=", rec.reconcile_part_id.id),
                                                          ("reconcile_id", "=", rec.reconcile_part_id.id)])
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
                    "total_amount": rec.debit,
                    "account_id": rec.account_id.id,
                    "reconcile_part_id": rec.reconcile_part_id.id,
                    "item_id": rec.id}

            debit.append((0, 0, data))

        return debit
