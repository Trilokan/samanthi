# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveAvailability(models.TransientModel):
    _name = "leave.availability"

    person_id = fields.Many2one(comodel_name="hos.person", string="Employee")
    leave_detail = fields.One2many(comodel_name="leave.availability.detail", inverse_name="available_id")

    @api.multi
    def onchange_person_id(self):
        if self.person_id.id:
            pass


class LeaveAvailabilityDetail(models.TransientModel):
    _name = "leave.availability.detail"

    available_id = fields.Many2one(comodel_name="leave.availability", string="Leave Type")
    leave_type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    available = fields.Float(string="Available")
