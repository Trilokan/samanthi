# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("received", "Received"), ("cancel", "Cancel")]
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
    received_by = fields.Many2one(comodel_name="hos.person", string="Person", readonly=True)
    receipt_detail = fields.One2many(comodel_name="material.receipt.detail",
                                     inverse_name="receipt_id", string="Receipt Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def trigger_inspection(self):
        pass

    @api.multi
    def trigger_confirm(self):
        writter = "Material Receipt confirmed by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Material Receipt cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

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
    quantity = fields.Float(string="Quantity", default=0, required=True)
    comment = fields.Text(string="Comment")
    receipt_id = fields.Many2one(comodel_name="material.receipt", string="Material Receipt")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="receipt_id.progress")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(MaterialReceiptDetail, self).create(vals)
