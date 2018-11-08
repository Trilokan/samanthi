# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductSubGroup(models.Model):
    _name = "product.sub.group"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    product_group_id = fields.Many2one(comodel_name="product.group", string="Product Group", required=True)

    _sql_constraints = [("code", "unique(code)", "Product Sub Group Code must be unique")]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.code, record.name)
            result.append((record.id, name))
        return result




