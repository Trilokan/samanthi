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
    operation_date = fields.Date(string="Date of Operation")
    patient_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    treatment_id = fields.Many2one(comodel_name="hos.treatment.in", string="Treatment")
    doctor_id = fields.Many2one(comodel_name="hos.person", string="Doctor")
    staff_id = fields.Many2many(comodel_name="hos.person", string="Staff")
    type_id = fields.Many2one(comodel_name="operation.type", string="Operation")
    theater_id = fields.Many2one(comodel_name="operation.theater", string="Operation Theater")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    procedure = fields.Binary(string="Operation Procedure")
    writter = fields.Text(string="Writter", track_visibility='always')

    @api.multi
    def trigger_paid(self):
        writter = "Accounts payable noted by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "paid", "writter": writter})

    @api.multi
    def trigger_scheduled(self):
        writter = "Operations Scheduled by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "scheduled", "writter": writter})

    @api.multi
    def trigger_done(self):
        writter = "Operations done by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "done", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Operations cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

    @api.multi
    def trigger_reschedule(self):
        writter = "Operation rescheduled by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "paid", "writter": writter})
