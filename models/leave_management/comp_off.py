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


class LeaveCompOff(models.Model):
    _name = "leave.comp.off"

    from_date = fields.Date(string="From Date", default=CURRENT_DATE, required=True)
    till_date = fields.Date(string="Till Date", default=CURRENT_DATE, required=True)
    person_id = fields.Many2one(comodel_name="qin.person", string="Person", required=True)
    reason = fields.Text(string="Reason")
    total_days = fields.Float(string="Total Days", default=0.0, required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
