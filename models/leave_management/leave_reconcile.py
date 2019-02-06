# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Confirmed'),
                 ('cancelled', 'Cancelled')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveReconcile(models.Model):
    _name = "leave.reconcile"

    name = fields.Char(string="Name")
    reconcile_ids = fields.One2many(comodel_name="leave.journal", inverse_name="reconcile_id")
    part_reconcile_ids = fields.One2many(comodel_name="leave.journal", inverse_name="part_reconcile_id")