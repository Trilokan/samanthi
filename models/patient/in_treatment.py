# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime
from .. import calculation

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Treatment Detail
class PatientTreatmentDetail(models.Model):
    _name = "in.treatment"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    description = fields.Text(string="Description", requied=True)
    unit = fields.Float(string="Units")
    comment = fields.Text(string="Comment", requied=True)
    in_patient_id = fields.Many2one(comodel_name="in.patient", string="Treatment")
