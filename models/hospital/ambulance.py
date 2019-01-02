# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("assigned", "Assigned"), ("done", "Done"), ("cancel", "Cancel")]
TRAVEL_TYPE = [("admission", "Admission"), ("shifting", "Shifting"), ("discharge", "Discharge")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class Ambulance(models.Model):
    _name = "hos.ambulance"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="lam.person", string="Patient")
    driver_id = fields.Many2one(comodel_name="lam.person", string="Driver")
    employee_ids = fields.Many2many(comodel_name="lam.person", string="Staff")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    travel_type = fields.Selection(selection=TRAVEL_TYPE, string="Travel Type", default="admission")

    # Source
    from_location = fields.Text(string="Source Location", required=True)
    from_time = fields.Datetime(string="Start Time", default=CURRENT_TIME)
    from_contact_person = fields.Char(string="Contact Person", required=True)
    from_contact_no = fields.Char(string="Contact No", required=True)

    # Destination
    to_location = fields.Text(string="Destination Location", required=True)
    to_time = fields.Datetime(string="End Time", default=CURRENT_TIME)
    to_contact_person = fields.Char(string="Contact Person", required=True)
    to_contact_no = fields.Char(string="Contact No", required=True)

    # Payment
    total_distance = fields.Float(string="Total Distance", default=0)
    total_hrs = fields.Float(string="Total Hrs", default=0)
    total_cost = fields.Float(string="Total Cost", default=0)

    writter = fields.Char(string="Writter", track_visibility="always")
