# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class JournalItems(models.Model):
    _name = "journal.items"

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

    @api.model
    def create(self, vals):
        if (vals["credit"] > 0) or (vals["debit"] > 0):
            vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
            return super(JournalItems, self).create(vals)
