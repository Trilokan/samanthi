# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"),
                 ('paid', 'Paid'),
                 ("scheduled", "Scheduled"),
                 ("done", "Done"),
                 ("cancel", "Cancel")]
THEATER_PROGRESS = [("draft", "Draft"), ("booked", "Booked"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class Operation(models.Model):
    _name = "hos.operation"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    doctor_id = fields.Many2many(comodel_name="hos.person", string="Doctor")
    staff_id = fields.Many2many(comodel_name="hos.person", string="Staff")
    type_id = fields.Many2one(comodel_name="operation.type", string="Operation")
    theater_id = fields.Many2one(comodel_name="operation.theater", string="Operation Theater")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    theater_progress = fields.Selection(selection=THEATER_PROGRESS, string="Progress")
    procedure = fields.Binary(string="Operation Procedure")

