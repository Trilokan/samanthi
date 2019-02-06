# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Waiting For Approval'),
                 ('cancelled', 'Cancelled'),
                 ('approved', 'Approved')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class PermissionApplication(models.Model):
    _name = "permission.application"

    date = fields.Date(string="Date", default=CURRENT_TIME, required=True)
    from_time = fields.Float(string="From Time", default=0.0, required=True)
    till_time = fields.Float(string="Till Time", default=0.0, required=True)
    person_id = fields.Many2one(comodel_name="qin.person", string="Person", required=True)
    reason = fields.Text(string="Reason")
    total_hours = fields.Float(string="Total Hours", default=0.0, required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
