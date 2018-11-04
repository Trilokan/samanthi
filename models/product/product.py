# -*- coding: utf-8 -*-

from odoo import models, fields


class Product(models.Model):
    _name = "hos.product"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    product_group_id = fields.Many2one(comodel_name="product.group", string="Group")
    product_sub_group_id = fields.Many2one(comodel_name="product.sub.group", string="Sub Group")
    category_id = fields.Many2one(comodel_name="product.category", string="Category")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM")
    hsn_code = fields.Char(string="HSN Code")
    

