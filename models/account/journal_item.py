# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
PROGRESS = [("draft", "Draft"), ("approved", "Approved")]


class JournalItem(models.Model):
    _name = "journal.item"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    journal_type_id = fields.Many2one(comodel_name="journal.type", string="Journal Type")
    invoice_id = fields.Many2one(comodel_name="qin.invoice", string="Invoice")
    person_id = fields.Many2one(comodel_name="qin.person", string="Person")
    account_id = fields.Many2one(comodel_name="qin.account", string="Account")
    description = fields.Text(string="Description")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    reconcile_id = fields.Many2one(comodel_name="qin.reconcile", string="Full Reconcile")
    part_reconcile_id = fields.Many2one(comodel_name="qin.reconcile", string="Partly Reconcile")

    @api.model
    def create(self, vals):
        if (vals["credit"] > 0) or (vals["debit"] > 0):
            vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
            return super(JournalItem, self).create(vals)
