# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("received", "Received"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class DirectMaterialReceipt(models.Model):
    _name = "direct.material.receipt"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    received_by = fields.Many2one(comodel_name="hos.person", string="Person", readonly=True)
    receipt_detail = fields.One2many(comodel_name="direct.material.receipt.detail",
                                     inverse_name="receipt_id", string="Receipt Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    invoice_flag = fields.Boolean(string="Invoice Generated")

    @api.multi
    def trigger_cancel(self):
        writter = "Direct Material Receipt cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

    def purchase_stock_move(self):
        recs = self.receipt_detail

        for rec in recs:
            pass

    def trigger_invoice_generation(self):
        pass

    def trigger_received(self):
        writter = "Direct Material Receipt by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "received", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(DirectMaterialReceipt, self).create(vals)


class DirectMaterialReceiptDeatil(models.Model):
    _name = "direct.material.receipt.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Item", required=True)
    description = fields.Text(string="Item Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity", default=0, required=True)
    comment = fields.Text(string="Comment")
    receipt_id = fields.Many2one(comodel_name="direct.material.receipt", string="Material Receipt")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="receipt_id.progress")

    @api.constrains
    def check_quantity(self):
        if self.quantity <= 0:
            raise exceptions.ValidationError("Error! Need Quantity")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(DirectMaterialReceiptDeatil, self).create(vals)
