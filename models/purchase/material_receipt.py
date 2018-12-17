# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("received", "Received"), ("inspected", "Inspected"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class MaterialReceipt(models.Model):
    _name = "material.receipt"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", readonly=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", readonly=True)
    po_id = fields.Many2one(comodel_name="purchase.order", string="Purchase Order", readonly=True)
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent", readonly=True)
    received_by = fields.Many2one(comodel_name="hos.person", string="Received By", readonly=True)
    inspected_by = fields.Many2one(comodel_name="hos.person", string="Inspected By", readonly=True)
    receipt_detail = fields.One2many(comodel_name="material.receipt.detail", inverse_name="receipt_id")
    invoice_flag = fields.Boolean(string="Invoice Flag")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def get_order_data(self, product_id, column):
        rec = self.env["purchase.order.detail"].search([("product_id", "=", product_id),
                                                        ("order_id", "=", self.po_id.id)])

        record = rec.copy_data()[0]
        return record[column]

    @api.multi
    def trigger_invoice_generation(self):
        recs = self.receipt_detail

        invoice_detail = []
        for rec in recs:
            invoice_detail.append((0, 0, {"product_id": rec.product_id.id,
                                          "description": rec.description,
                                          "quantity": rec.quantity,
                                          "discount": self.get_order_data(rec.product_id.id, "discount"),
                                          "tax_id": self.get_order_data(rec.product_id.id, "tax_id"),
                                          "unit_price": self.get_order_data(rec.product_id.id, "unit_price")}))

        if invoice_detail:
            invoice = {"person_id": self.person_id.id,
                       "indent_id": self.indent_id.id,
                       "po_id": self.po_id.id,
                       "receipt_id": self.id,
                       "invoice_type": "po",
                       "invoice_detail": invoice_detail}

            self.env["purchase.invoice"].create(invoice)

    @api.multi
    def trigger_cancel(self):
        writter = "Material Receipt cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

    def generate_move(self, recs):
        config = self.env["product.configuration"].search([("company_id", "=", self.env.user.company_id.id)])

        source_id = config.purchase_id.id
        destination_id = config.store_id.id

        for rec in recs:
            result = {"source_id": source_id,
                      "destination_id": destination_id,
                      "reference": rec.name,
                      "product_id": rec.product_id.id,
                      "description": rec.description,
                      "quantity": rec.quantity,
                      "progress": "moved"}

            self.env["hos.move"].create(result)

    def generate_remaining(self):
        receipt_detail = []
        recs = self.receipt_detail
        for rec in recs:
            received_quantity = rec.received_quantity + rec.quantity
            if rec.requested_quantity > received_quantity:
                receipt_detail.append((0, 0, {"product_id": rec.product_id.id,
                                              "description": rec.description,
                                              "requested_quantity": rec.requested_quantity,
                                              "received_quantity": received_quantity}))

        if receipt_detail:
            receipt = {"person_id": self.person_id.id,
                       "po_id": self.po_id.id,
                       "indent_id": self.indent_id.id,
                       "receipt_detail": receipt_detail}

            self.env["material.receipt"].create(receipt)

    @api.multi
    def trigger_inspection(self):
        inspected_by = self.env.user.person_id.id
        recs = self.env["material.receipt.detail"].search([("receipt_id", "=", self.id), ("quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_move(recs)
        self.generate_remaining()

        writter = "Material Receipt inspected by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "inspected", "writter": writter, "inspected_by": inspected_by})

    @api.multi
    def trigger_received(self):
        received_by = self.env.user.person_id.id
        writter = "Material Receipt by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "received", "writter": writter, "received_by": received_by})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(MaterialReceipt, self).create(vals)


class MaterialReceiptDetail(models.Model):
    _name = "material.receipt.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Item", required=True)
    description = fields.Text(string="Item Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    requested_quantity = fields.Float(string="Order Quantity", default=0, readonly=True)
    received_quantity = fields.Float(string="Received Quantity", default=0, readonly=True)
    receiving_quantity = fields.Float(string="Receiving Quantity", default=0, required=True)
    quantity = fields.Float(string="Quantity", default=0, required=True)
    comment = fields.Text(string="Comment")
    receipt_id = fields.Many2one(comodel_name="material.receipt", string="Material Receipt")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="receipt_id.progress")

    @api.constrains("quantity")
    def check_issue_quantity(self):
        if self.quantity > (self.requested_quantity - self.received_quantity):
            raise exceptions.ValidationError("Error! Received quantity more than Order quantity")

        if self.quantity > self.receiving_quantity:
            raise exceptions.ValidationError("Error! Receiving quantity more than Order quantity")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(MaterialReceiptDetail, self).create(vals)
