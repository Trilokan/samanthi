# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
PROGRESS = [("draft", "Draft"), ("approved", "Approved")]


class QinJournal(models.Model):
    _name = "qin.journal"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", required=True)
    period_id = fields.Many2one(comodel_name="qin.period", string="Period")
    journal_type_id = fields.Many2one(comodel_name="qin.period", string="Journal Type")
    progress = fields.Selection(selection=PROGRESS, string="Progress", default="draft")
    reference = fields.Char(string="Reference")
    item_ids = fields.One2many(comodel_name="journal.item", inverse_name="journal_id")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(QinJournal, self).create(vals)
