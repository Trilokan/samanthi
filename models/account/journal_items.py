# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class JournalItems(models.Model):
    _name = "journal.items"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    description = fields.Text(string="Description")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    credit = fields.Float(string="Credit", default=0, required=True)
    debit = fields.Float(string="Debit", default=0, required=True)
    reconcile_id = fields.Many2one(comodel_name="hos.reconcile", string="Reconcile")
    reconcile_part_id = fields.Many2one(comodel_name="hos.reconcile", string="Partial Reconcile")
    entry_id = fields.Many2one(comodel_name="journal.entries", string="Journal Entry")
    active = fields.Boolean(string="Active", default=True)

    def payable_lines(self, account_id):
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

    def receivable_lines(self, account_id):
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

    @api.model
    def create(self, vals):
        if (vals["credit"] > 0) or (vals["debit"] < 0):
            vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
            return super(JournalItems, self).create(vals)
