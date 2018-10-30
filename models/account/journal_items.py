# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JournalItems(models.Model):
    _name = "journal.items"

    name = fields.Char(string="Name")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    reconcile_id = fields.Many2one(comodel_name="hos.reconciliation", string="Reconcile")
    reconcile_part_id = fields.Many2one(comodel_name="hos.reconciliation", string="Partial Reconcile")
    entry_id = fields.Many2one(comodel_name="journal.entries", string="Journal Entry")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")

    def get_un_reconcile_items(self, account_id, voucher_id):
        credit_items = []
        debit_items = []

        recs = self.env["journal.items"].search([("account_id", "=", account_id.id),
                                                 ("reconcile_id", "=", False),
                                                 ("reconcile_part_id", "=", False)])

        for rec in recs:
            amount = rec.credit or rec.debit
            if amount:

                data = {"description": rec.name,
                        "total_amount": amount,
                        "opening_amount": amount,
                        "item_id": rec.id}

                if rec.credit:
                    data["credit_id"] = voucher_id
                    credit_items.append((0, 0, data))

                if rec.debit:
                    data["debit_id"] = voucher_id
                    debit_items.append((0, 0, data))

        return credit_items, debit_items

    def get_partly_reconcile_items(self, account_id):
        credit_items = []
        debit_items = []

        part_reconcile_ids = self.env["journal.items"].search([("account_id", "=", account_id.id),
                                                               ("reconcile_id", "=", False),
                                                               ("reconcile_part_id", "=", True)])

        recs = part_reconcile_ids.ids
        recs = list(set(recs))

        for rec_id in recs:
            data = self.get_reconcile_data(rec_id)


    def get_reconcile_data(self, rec_id):
        recs = self.env["journal.items"].search([("reconcile_part_id", "=", rec_id)])

        credit_amount = debit_amount = 0
        credit_data = {}
        debit_data = {}

        for rec in recs:
            credit_amount = credit_amount + rec.credit
            debit_amount = debit_amount + rec.debit

        if credit_amount > debit_amount:
            item = self.env["journal.items"].search([("reconcile_part_id", "=", rec_id),
                                                     ("credit", ">", 0)])

            credit_data = {"description": item.name,
                    "total_amount": item.credit,
                    "opening_amount": debit_amount,
                    "item_id": rec.id}

        else:
            item = self.env["journal.items"].search([("reconcile_part_id", "=", rec_id),
                                                     ("debit", ">", 0)])

            debit_data = {"description": item.name,
                          "total_amount": item.credit,
                          "opening_amount": credit_amount,
                          "item_id": rec.id}

        return credit_data, debit_data

    @api.multi
    def get_items(self, account_id, voucher_id):
        """
        :param account_id:
        :return: unreconciled and partly reconciled items

        """
        credit, debit = self.get_un_reconcile_items(account_id, voucher_id)

        return credit, debit


