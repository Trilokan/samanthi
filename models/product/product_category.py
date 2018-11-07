# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductCategory(models.Model):
    _name = "product.category"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    description = fields.Text(string="Description")

    _sql_constraints = [
        ("code", "unique(code)", "Product Category must be unique"),
    ]



