# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreRequest(models.Model):
    _name = "store.request"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    department_id = fields.Many2one(comodel_name="hos.department", string="Department", required=True)
    request_by = fields.Many2one(comodel_name="hos.person", string="Request By", readonly=True)
    approve_by = fields.Many2one(comodel_name="hos.person", string="Approve By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    request_detail = fields.One2many(comodel_name="store.request.detail", inverse_name="request_id", string="Request Detail")
    writter = fields.Char(string="Writter", track_visibility="always")


class StoreRequestDetail(models.Model):
    _name = "store.request.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    requested_quantity = fields.Float(string="Request Quantity")
    quantity = fields.Float(string="Quantity")
    request_id = fields.Many2one(comodel_name="store.request", string="Store Request")
