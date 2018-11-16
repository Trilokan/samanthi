# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime
from .. import calculation

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
MEDICINE_TYPE = [("after_food", "After Food"), ("before_food", "Before Food")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Prescription
class PatientPrescription(models.Model):
    _name = "patient.prescription"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date", default=CURRENT_TIME, required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    total_days = fields.Float(string="Days")
    prescription_detail = fields.One2many(comodel_name="patient.prescription.detail", inverse_name="prescription_id")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")


class PatientPrescriptionDetail(models.Model):
    _name = "patient.prescription.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product")
    morning = fields.Boolean(string="Morning")
    noon = fields.Boolean(string="Noon")
    night = fields.Boolean(string="Night")
    prescription_id = fields.Many2one(comodel_name="patient.prescription", string="Prescription")
    medicine_type = fields.Selection(selection=MEDICINE_TYPE, string="Medicine Type")
    quantity = fields.Integer(string="Quantity")


