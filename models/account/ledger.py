# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Ledger(models.TransientModel):
    _name = "hos.ledger"

    from_date = fields.Date(string="From Date")
    till_date = fields.Date(string="Till Date")
    journal_id = fields.Many2one(comodel_name="hos.journal", string="Journal")

