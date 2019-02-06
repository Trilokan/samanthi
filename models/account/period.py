# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .. import calculation as cal
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
            if rec.name:
                month = rec.name.split(" ")
                rec.financial_year = month[1]

        return True

    @api.model
    def create(self, vals):
        start = datetime.strptime(vals["name"], "%B %Y")
        end = start + relativedelta(months=1) - timedelta(days=1)
        vals["start_date"] = start.strftime("%Y-%m-%d")
        vals["end_date"] = end.strftime("%Y-%m-%d")

        return super(QinPeriod, self).create(vals)

