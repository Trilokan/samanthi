# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockWarehouse(models.Model):
    _name = "stock.warehouse"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", readonly=True)
    location_id = fields.Many2one(comodel_name="stock.location", string="Location", readonly=True)
    quantity = fields.Float(string="Quantity", compute="_get_stock")

    def _get_stock(self):
        for record in self:
            record.quantity = self.env["hos.stock"].get_current_stock(record.product_id.id, record.location_id.id)

    @api.model
    def create(self, vals):
        record = self.env["stock.warehouse"].search_count([("product_id", "=", vals["product_id"]),
                                                           ("location_id", "=", vals["location_id"])])

        if not record:
            return super(StockWarehouse, self).create(vals)
