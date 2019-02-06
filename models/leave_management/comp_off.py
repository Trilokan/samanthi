# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Waiting For Approval'),
                 ('cancelled', 'Cancelled'),
                 ('approved', 'Approved')]
TOTAL_DAYS = [("half_day", "Half Day"), ("full_day", "Full Day")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class CompOffApplication(models.Model):
    _name = "comp.off.application"

    date = fields.Date(string="From Date", default=CURRENT_DATE, required=True)
    person_id = fields.Many2one(comodel_name="qin.person", string="Person", required=True)
    reason = fields.Text(string="Reason")
    total_days = fields.Selection(selection=TOTAL_DAYS, string="Total Days", default="full_day", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
