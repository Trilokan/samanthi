# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class HosMove(models.Model):
    _name = "hos.move"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    source_id = fields.Many2one(comodel_name="stock.location", string="Source Location", required=True)
    destination_id = fields.Many2one(comodel_name="stock.location", string="Source Location", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    reference = fields.Text(string="Reference")
    picking_id = fields.Many2one(comodel_name="hos.picking", string="Picking")
