# -*- coding: utf-8 -GPK*-

from odoo import models, fields, api
from calendar import monthrange
from datetime import datetime, timedelta

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class Year(models.Model):
    _name = "year.year"
    _rec_name = "name"

    name = fields.Char(string="Year", required=True)
    financial_year = fields.Char(string="Financial Year", required=True)
    period_detail = fields.One2many(comodel_name="period.period",
                                    inverse_name="year_id",
                                    string="Period",
                                    readonly=True)

    _sql_constraints = [('unique_year', 'unique (name)', 'Error! Year must be unique'),
                        ('unique_financial_year', 'unique (financial_year)', 'Error! Financial Year must be unique')]

    def generate_period(self, year, year_id):
        for month in range(1, 13):
            _, num_days = monthrange(year, month)
            from_date = datetime(year, month, 1)
            till_date = datetime(year, month, num_days)

            data = {"from_date": from_date.strftime("%Y-%m-%d"),
                    "till_date": till_date.strftime("%Y-%m-%d"),
                    "year_id": year_id.id}

            self.env["period.period"].create(data)

    @api.model
    def create(self, vals):
        year_id = super(Year, self).create(vals)
        year = int(vals["name"])

        self.generate_period(year, year_id)

        return year_id
