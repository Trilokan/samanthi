# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductUOM(models.Model):
    _name = "product.uom"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    _sql_constraints = [
        ("code", "unique(code)", "Unit Of Measurement must be unique"),
    ]


