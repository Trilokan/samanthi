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
    reference = fields.Char(string="Reference")

    @api.model
    def create(self, vals):
        print vals
        # return super(JournalItems, self).create(vals)
