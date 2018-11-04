# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class Invoice(models.Model):
    _name = "hos.invoice"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    person_id = ""
    gst_no = ""
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    invoice_detail = fields.One2many(comodel_name="invoice.detail", inverse_name="invoice_id", string="Invoice Detail")
    cgst = fields.Float(string="CGST")
    sgst = fields.Float(string="SGST")
    igst = fields.Float(string="IGST")
    sub_total = fields.Float(string="Sub Total")
    discount_amount = fields.Float(string="Discount Amount")
    taxed_amount = fields.Float(string="Taxed Amount")
    untaxed_amount = fields.Float(string="Untaxed Amount")
    total = fields.Float(string="Total")

    writter = fields.Char(string="Writter", track_visibility="always")


class InvoiceDetail(models.Model):
    _name = "invoice.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    requested_quantity = fields.Float(string="Request Quantity")
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    discount = fields.Float(string="Unit Price")
    tax_id = fields.Many2one(comodel_name="product.tax", string="Tax")
    total = fields.Float(string="Unit Price")
    invoice_id = fields.Many2one(comodel_name="invoice.detail", string="Invoice")
