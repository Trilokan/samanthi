# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime, timedelta


# Work Leave
class WorkLeave(models.Model):
    _name = "work.leave"
    _inherit = "mail.thread"
    _order = "sequence"

    sequence = fields.Integer(string="Sequence")
    type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    work_id = fields.Many2one(comodel_name="work.detail", string="Work Detail")
    opening = fields.Float(string="Opening", default=0.0)
    credit = fields.Float(string="Credit", default=0.0)
    reconcile = fields.Float(string="Reconcile", default=0.0)
    closing = fields.Float(string="Closing", default=0.0)
