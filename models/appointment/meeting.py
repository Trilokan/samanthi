# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Meeting
class AppointmentMeeting(models.Model):
    _name = "appointment.meeting"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date", default=CURRENT_TIME, required=True)
    employee_id = fields.Many2one(comodel_name="hos.person", string="Employee", required=True)
    reason = fields.Many2one(comodel_name="appointment.reason", string="Reason", required=True, domain=[("meeting", "=", True)])
    comment = fields.Text(string="Comment")
    writter = fields.Text(string="Writter", track_visibility='always')

    @api.model
    def create(self, vals):
        vals["writter"] = "Meeting scheduled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        return super(AppointmentMeeting, self).create(vals)

