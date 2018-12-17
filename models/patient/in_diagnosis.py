# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime
from .. import calculation

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Diagnosis
class InPatientDiagnosis(models.Model):
    _name = "in.diagnosis"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    diagnosis_id = fields.Many2one(comodel_name="patient.diagnosis", string="Diagnosis")
    in_patient_id = fields.Many2one(comodel_name="in.patient", string="Treatment")
    comment = fields.Text(string="Comment")
