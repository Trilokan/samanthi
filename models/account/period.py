# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .. import calculation as cal

PROGRESS = [("draft", "Draft"), ("open", "Open"), ("closed", "Closed")]


class QinPeriod(models.Model):
    _name = "qin.period"

    name = fields.Selection(selection=cal.get_months(), string="Month", required=True)
    start_date = fields.Date(string="Start Date", readonly=True)
    end_date = fields.Date(string="End Date", readonly=True)
    financial_year = fields.Char(string="Financial Year", compute="_cal_financial_year")
    progress = fields.Selection(selection=PROGRESS, string="Progress", default="draft")

    _sql_constraints = [("name", "unique(name)", "Period must be unique")]

    @api.multi
    def _cal_financial_year(self):
        for rec in self:
            if self.name:
                rec.financial_year = ""

        return True

