# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("accepted", "Accepted"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreAccept(models.Model):
    _name = "store.accept"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    return_id = fields.Many2one(comodel_name="store.return", string="Return", required=True)
    issue_by = fields.Many2one(comodel_name="hos.person", string="Accepted By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    accept_detail = fields.One2many(comodel_name="store.accept.detail", inverse_name="accept_id", string="Accept Detail")
    writter = fields.Char(string="Writter", track_visibility="always")


class StoreAcceptDetail(models.Model):
    _name = "store.accept.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity")
    accept_id = fields.Many2one(comodel_name="store.accept", string="Store Accept")
