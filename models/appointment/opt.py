# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Out-Patient Appointment
class AppointmentOPT(models.Model):
    _name = "appointment.opt"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date", default=CURRENT_TIME, required=True)
    employee_id = fields.Many2one(comodel_name="lam.person", string="Doctor", required=True)
    patient_id = fields.Many2one(comodel_name="lam.person", string="Patient", required=True)
    reason = fields.Many2one(comodel_name="appointment.reason", string="Reason", required=True, domain=[("meeting", "=", False)])
    comment = fields.Text(string="Comment")
    writter = fields.Text(string="Writter", track_visibility='always')

    @api.model
    def create(self, vals):
        vals["writter"] = "OPT scheduled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        return super(AppointmentOPT, self).create(vals)

