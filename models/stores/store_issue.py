# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("issued", "Issued"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreIssue(models.Model):
    _name = "store.issue"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    request_id = fields.Many2one(comodel_name="store.request", string="Request", required=True)
    issue_by = fields.Many2one(comodel_name="hos.person", string="Issue By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    issue_detail = fields.One2many(comodel_name="store.issue.detail", inverse_name="issue_id", string="Issue Detail")
    writter = fields.Char(string="Writter", track_visibility="always")


class StoreIssueDetail(models.Model):
    _name = "store.issue.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity")
    issue_id = fields.Many2one(comodel_name="store.issue", string="Store Issue")
