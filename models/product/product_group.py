# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductGroup(models.Model):
    _name = "product.group"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    _sql_constraints = [
        ("code", "unique(code)", "Product Group Code must be unique"),
    ]
