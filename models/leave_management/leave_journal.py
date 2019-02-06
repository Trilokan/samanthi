# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Confirmed'),
                 ('cancelled', 'Cancelled')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveJournal(models.Model):
    _name = "leave.journal"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    person_id = fields.Many2one(comodel_name="qin.person", string="Person", required=True)
    leave_type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type", required=True)
    description = fields.Text(string="Description")
    reference = fields.Text(string="Reference")
    total_days = fields.Float(string="Total Days", default=0.0, required=True)
    reconcile_id = fields.Many2one(comodel_name="leave.reconcile", string="Full Reconcile")
    part_reconcile_id = fields.Many2one(comodel_name="leave.reconcile", string="Partly Reconcile")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
