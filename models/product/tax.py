# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTax(models.Model):
    _name = "product.tax"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    rate = fields.Float(string="Rate", default=0, required=True)

    _sql_constraints = [("code", "unique(code)", "Tax must be unique")]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "{0}-{1}%".format(record.code, record.name)
            result.append((record.id, name))
        return result


