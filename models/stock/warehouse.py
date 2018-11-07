# -*- coding: utf-8 -*-

from odoo import models, fields


class StockWarehouse(models.Model):
    _name = "stock.warehouse"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", readonly=True)
    location_id = fields.Many2one(comodel_name="stock.location", string="Location", readonly=True)
    quantity = fields.Float(string="Quantity", compute="_get_stock")

    _sql_constraints = [('product_location', 'unique (product_id, location_id)', 'Error! Product location must be unique')]

    def _get_stock(self):
        for record in self:
            source = [("product_id", "=", record.product_id.id),
                      ("source_location_id", "=", record.location_id.id),
                      ("progress", "=", "moved")]

            destination = [("product_id", "=", record.product_id.id),
                           ("destination_location_id", "=", record.location_id.id),
                           ("progress", "=", "moved")]

            record.quantity = self.env["hos.stock"].get_stock(source, destination)
