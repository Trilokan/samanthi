# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class HospitalReminder(models.Model):
    _name = "hos.reminder"
    _rec_name = "person_id"

    date = fields.Datetime(string="Date", default=CURRENT_TIME, required=True)
    person_id = fields.Many2one(comodel_name="hos.person",
                                string="Name",
                                default=lambda self: self.env.user.person_id.id,
                                required=True)
    message = fields.Text(string="Message", required=True)

