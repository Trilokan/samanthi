# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JournalEntries(models.Model):
    _name = "journal.entries"

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    # period_id = fields.Many2one(comodel_name="hos.period", string="Period")
    item_ids = fields.One2many(comodel_name="journal.items", inverse_name="entry_id",
                               string="Journal Items")
