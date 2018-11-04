# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductLocation(models.Model):
    _name = "product.location"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    _sql_constraints = [
        ("code", "unique(code)", "Product Location must be unique"),
    ]


