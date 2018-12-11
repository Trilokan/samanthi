# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime
from .. import calculation

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Patient Shifting
class PatientShifting(models.Model):
    _name = "patient.shifting"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date", default=CURRENT_TIME, required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    source_id = fields.Many2one(comodel_name="hos.bed", string="Source", required=True)
    destination_id = fields.Many2one(comodel_name="hos.bed", string="Destination ", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

