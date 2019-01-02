# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class InPatientTreatment(models.Model):
    _name = "in.patient"

    date = fields.Datetime(string="Date", required=True)
    patient_id = fields.Many2one(comodel_name="lam.person", string="Patient")
    patient_uid = fields.Char(string="", related="")
    age = fields.Char(string="", related="")
    mobile = fields.Char(string="", related="")

    prescription_ids = fields.One2many(comodel_name="patient.prescription", inverse_name="in_patient_id")
    treatment_ids = fields.One2many(comodel_name="in.treatment", inverse_name="in_patient_id")
    diagnosis_ids = fields.One2many(comodel_name="in.diagnosis", inverse_name="in_patient_id")
    treatment_report = fields.Html(string="Treatment Report")
