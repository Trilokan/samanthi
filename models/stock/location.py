# -*- coding: utf-8 -*-

from odoo import models, fields


class StockLocation(models.Model):
    _name = "stock.location"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    _sql_constraints = [("code", "unique(code)", "Stock Location must be unique")]


