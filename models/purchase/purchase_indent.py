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
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    requested_by = fields.Many2one(comodel_name="qin.person", string="Request By", readonly=True)
    approved_by = fields.Many2one(comodel_name="qin.person", string="Approve By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    indent_detail = fields.One2many(comodel_name="purchase.indent.detail", inverse_name="indent_id")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        writter = "Purchase Indent Confirmed by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Purchase Indent cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

    @api.multi
    def trigger_approve(self):
        recs = self.env["purchase.indent.detail"].search([("indent_id", "=", self.id), ("quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        writter = "Purchase Indent Approved by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "approved", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(PurchaseIndent, self).create(vals)


class PurchaseIndentDetail(models.Model):
    _name = "purchase.indent.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="qin.product", string="Product", required=True)
    description = fields.Text(string="Item Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    requested_quantity = fields.Float(string="Request Quantity", default=0, required=True)
    quantity = fields.Float(string="Quantity", default=0, required=True)
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="indent_id.progress")

    @api.constrains("quantity")
    def check_requested_quantity(self):
        if self.quantity > self.requested_quantity:
            raise exceptions.ValidationError("Error! Approved quantity more than requested")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(PurchaseIndentDetail, self).create(vals)
