# -*- coding: utf-8 -*-

# Invoice generator based on the multiple Indent clubbed into one quotation
# Receipt tracking based on this only


from odoo import fields, models, api, exceptions, _
from datetime import datetime


class InvoiceGenerator(models.TransientModel):
    _name = "invoice.generator"

    order_id = fields.Many2one(comodel_name="purchase.order", string="Purchase order", required=True)
    receipt_ids = fields.Many2many(comodel_name="material.receipt", string="Material Receipt", required=True)

    def get_quantity(self, product_id):
        recs = self.env["material.receipt.detail"].search([("receipt_id", "in", self.receipt_ids.ids),
                                                           ("product_id", "=", product_id)])

        quantity = sum(recs.mapped('quantity'))
        return quantity

    def trigger_invoice_generation(self):
        items = self.order_id.order_detail

        invoice_detail = []
        for item in items:
            invoice_detail.append((0, 0, {"product_id": item.product_id.id,
                                          "description": item.description,
                                          "discount": item.discount,
                                          "quantity": self.get_quantity(item.product_id.id),
                                          "tax_id": item.tax_id.id,
                                          "unit_price": item.unit_price}))

        if invoice_detail:
            invoice = {"person_id": self.order_id.person_id.id,
                       "po_id": self.order_id.id,
                       "invoice_type": "po",
                       "invoice_detail": invoice_detail}

            self.env["purchase.invoice"].create(invoice)
