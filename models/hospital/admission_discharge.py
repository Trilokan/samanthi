# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime

ADMISSION_INFO = [("draft", "Draft"), ("admitted", "Admitted")]
DISCHARGE_INFO = [("draft", "Draft"), ("admitted", "Admitted"), ("discharged", "Discharged")]


class AdmissionDischarge(models.Model):
    _name = "admission.discharge"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    person_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    progress = fields.Selection()
    admission_type = ""
    reason = ""

    admitted_by = ""

    contact = ""
    email = ""
    alternate_contact = ""



