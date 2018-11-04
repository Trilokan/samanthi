# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductSubGroup(models.Model):
    _name = "product.sub.group"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    _sql_constraints = [
        ("code", "unique(code)", "Product Sub Group Code must be unique"),
    ]


