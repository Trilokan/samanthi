# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class PurchaseIndent(models.Model):
    _name = "purchase.indent"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    department_id = fields.Many2one(comodel_name="hos.department", string="Department", required=True)
    request_by = fields.Many2one(comodel_name="hos.person", string="Request By", readonly=True)
    approve_by = fields.Many2one(comodel_name="hos.person", string="Approve By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    indent_detail = fields.One2many(comodel_name="purchase.indent.detail", inverse_name="request_id", string="Request Detail")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        writter = "Store Request Confirmed by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Store Request cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

    def get_last_5_invoice_transaction(self, product_id):
        history = []
        recs = self.env["purchase.invoice.detail"].search([("product_id", "=", product_id)])

        for rec in recs:
            if len(history) < 5:
                data = rec.copy_data()[0]
                history.append((0, 0, data))

        return history

    @api.multi
    def generate_quote(self, recs):
        quote_detail = []
        for rec in recs:
            quote_detail.append((0, 0, {"product_id": rec.product_id.id,
                                        "quantity": rec.quantity,
                                        "purchase_history": self.get_last_5_invoice_transaction(rec.product_id.id)}))

        if quote_detail:
            quote = {"indent_id": self.id,
                     "quote_detail": quote_detail}

            self.env["purchase.quote"].create(quote)

        return quote_detail

    @api.multi
    def trigger_approved(self):
        recs = self.env["purchase.indent.detail"].search([("indent_id", "=", self.id), ("quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_quote(recs)

        writter = "Purchase Indent Approved by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "approved", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(PurchaseIndent, self).create(vals)


class PurchaseIndentDetail(models.Model):
    _name = "purchase.indent.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    requested_quantity = fields.Float(string="Request Quantity")
    quantity = fields.Float(string="Quantity")
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent")
