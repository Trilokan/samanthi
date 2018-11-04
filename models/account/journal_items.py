# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JournalItems(models.Model):
    _name = "journal.items"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    reconcile_id = fields.Many2one(comodel_name="hos.reconcile", string="Reconcile")
    reconcile_part_id = fields.Many2one(comodel_name="hos.reconcile", string="Partial Reconcile")
    entry_id = fields.Many2one(comodel_name="journal.entries", string="Journal Entry")
    active = fields.Boolean(string="Active", default=True)

