# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class PurchaseInvoice(models.Model):
    _name = "purchase.invoice"
    _inherit = "mail.thread"

    date = ""
    name = ""
    person_id = ""
    po_id = ""
    receipt_id = ""
    indent_id = ""


class PurchaseInvoiceDetail(models.Model):
    _name = ""

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Item", required=True)
    description = fields.Text(string="Item Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity", default=0, required=True)
    unit_pri
    comment = fields.Text(string="Comment")
    receipt_id = fields.Many2one(comodel_name="direct.material.receipt", string="Material Receipt")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="receipt_id.progress")


