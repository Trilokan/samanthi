# -*- coding: utf-8 -*-

from odoo import fields, models


# Stock
class Stock(models.Model):
    _name = "hos.stock"

    def get_stock(self, search_source, search_destination):
        source_ids = self.env["hos.move"].search(search_source)
        destination_ids = self.env["hos.move"].search(search_destination)

        quantity_in = sum(source_ids.mapped("quantity"))
        quantity_out = sum(destination_ids.mapped("quantity"))

        return quantity_in - quantity_out

    def get_current_stock(self, product_id, location_id):
        source_ids = self.env["hos.move"].search([("product_id", "=", product_id),
                                                  ("source_id", "=", location_id),
                                                  ("progress", "=", "moved")])

        destination_ids = self.env["hos.move"].search([("product_id", "=", product_id),
                                                       ("destination_id", "=", location_id),
                                                       ("progress", "=", "moved")])

        quantity_in = sum(source_ids.mapped("quantity"))
        quantity_out = sum(destination_ids.mapped("quantity"))

        return quantity_in - quantity_out
