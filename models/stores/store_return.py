# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreReturn(models.Model):
    _name = "store.return"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, deafult=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    department_id = fields.Many2one(comodel_name="hos.department", string="Department", required=True)
    return_by = fields.Many2one(comodel_name="hos.person", string="Return By", readonly=True)
    approve_by = fields.Many2one(comodel_name="hos.person", string="Approve By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    return_detail = fields.One2many(comodel_name="store.return.detail", inverse_name="return_id", string="Return Detail")
    writter = fields.Char(string="Writter", track_visibility="always")


class StoreReturnDetail(models.Model):
    _name = "store.return.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    returned_quantity = fields.Float(string="Return Quantity")
    quantity = fields.Float(string="Quantity")
    return_id = fields.Many2one(comodel_name="store.return", string="Store Return")
