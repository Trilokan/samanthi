# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime

ADMISSION_INFO = [("draft", "Draft"), ("admitted", "Admitted")]
DISCHARGE_INFO = [("draft", "Draft"), ("admitted", "Admitted"), ("discharged", "Discharged")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class AdmissionDischarge(models.Model):
    _name = "admission.discharge"

    date = fields.Date(string="Date", required=True)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    admission_progress = fields.Selection(selection=ADMISSION_INFO, default="draft")
    discharge_progress = fields.Selection(selection=DISCHARGE_INFO, default="draft")




