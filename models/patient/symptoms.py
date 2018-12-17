# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime
from .. import calculation


CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Symptoms
class PatientSymptoms(models.Model):
    _name = "patient.symptoms"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", readonly=True)
    image = fields.Binary(string="Image")
    description = fields.Html(string="Description", required=True)
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
