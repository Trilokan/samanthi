# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class JournalEntries(models.Model):
    _name = "journal.entries"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    journal_id = fields.Many2one(comodel_name="hos.journal", string="Journal", required=True)
    period_id = fields.Many2one(comodel_name="period.period", string="Period", required=True)
    reference = fields.Char(string="Reference")
    item_ids = fields.One2many(comodel_name="journal.items", inverse_name="entry_id",
                               string="Journal Items")

    @api.constrains("item_ids")
    def check_item_ids(self):
        pass

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(JournalEntries, self).create(vals)
