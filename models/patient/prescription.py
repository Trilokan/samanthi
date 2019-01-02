# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime
from .. import calculation

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
CONSUMPTION_TYPE = [("after_food", "After Food"), ("before_food", "Before Food")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Prescription
class PatientPrescription(models.Model):
    _name = "patient.prescription"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date", default=CURRENT_TIME, required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="lam.person", string="Person")
    total_days = fields.Float(string="Days")
    prescription_detail = fields.One2many(comodel_name="patient.prescription.detail", inverse_name="prescription_id")
    in_patient_id = fields.Many2one(comodel_name="in.patient", string="Treatment")


class PatientPrescriptionDetail(models.Model):
    _name = "patient.prescription.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Medicine")
    morning = fields.Boolean(string="FN")
    noon = fields.Boolean(string="Noon")
    night = fields.Boolean(string="AN")
    prescription_id = fields.Many2one(comodel_name="patient.prescription", string="Prescription")
    consumption_type = fields.Selection(selection=CONSUMPTION_TYPE, string="Consumption Type")
    quantity = fields.Integer(string="Quantity")


