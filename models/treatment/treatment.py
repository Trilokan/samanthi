# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime
from .. import calculation


PROGRESS_INFO = [('draft', 'Draft'), ('approved', 'approved'), ('cancel', 'Cancel')]
INVOICE_TYPE = [("dpo", "Direct Purchase Bill"), ("po", "Purchase Bill")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Bills
class PatientTreatment(models.Model):
    _name = "patient.treatment"
    _inherit = "mail.thread"

    date = fields.Date(srring="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)

    patient_id = fields.Many2one(comodel_name="hos.patient", string="Patient")
    symptoms_ids = fields.One2many(comodel_name="patient.symptoms", inverse_name="treatment_id")
    diagnosis_ids = fields.One2many(comodel_name="patient.diagnosis", inverse_name="diagnosis_id")
    treatment_detail = fields.One2many(comodel_name="", inverse_name="")
    visit_detail = fields.One2many(comodel_name="", inverse_name="")
    reminder_detail = fields.One2many(comodel_name="", inverse_name="")
    bed_shift_detail = fields.One2many(comodel_name="", inverse_name="")
    prescription_ids = fields.One2many(comodel_name="", inverse_name="")


