# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"),
                 ('paid', 'Paid'),
                 ("scheduled", "Scheduled"),
                 ("done", "Done"),
                 ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class Operation(models.Model):
    _name = "hos.operation"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    image = fields.Binary(string="Image")
    name = fields.Char(string="Name", readonly=True)
    operation_date = fields.Date(string="Date")
    patient_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    treatment_id = fields.Many2one(comodel_name="hos.treatment.in", string="Treatment")
    doctor_id = fields.Many2one(comodel_name="hos.person", string="Doctor")
    staff_id = fields.Many2many(comodel_name="hos.person", string="Staff")
    type_id = fields.Many2one(comodel_name="operation.type", string="Operation")
    theater_id = fields.Many2one(comodel_name="operation.theater", string="Operation Theater")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    procedure = fields.Binary(string="Operation Procedure")

    @api.multi
    def trigger_paid(self):
        self.write({"progress": "paid"})

    @api.multi
    def trigger_scheduled(self):
        self.write({"progress": "scheduled"})

    @api.multi
    def trigger_done(self):
        self.write({"progress": "done"})

    @api.multi
    def trigger_cancel(self):
        self.write({"progress": "cancel"})
