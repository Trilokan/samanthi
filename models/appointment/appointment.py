# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancel")]
SCHEDULE_TYPE = [("opt", "Out Patient Treatment"),
                 ("ot", "Operation Theater"),
                 ("meetings", "Meetings"),
                 ("others", "Others")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Appointment
class HospitalAppointment(models.Model):
    _name = "hos.appointment"
    _inherit = "mail.thread"

    employee_id = fields.Many2one(comodel_name="hos.person", string="Employee", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    appointment_time = fields.Datetime(string="Time", default=CURRENT_TIME, required=True)
    appointment_type = fields.Selection(selection=SCHEDULE_TYPE, string="Schedule Type", required=True)
    reason = fields.Many2one(comodel_name="appointment.reason", string="Reason", required=True)
    ot_id = fields.Many2one(comodel_name="hos.operation", string="Operation Theater")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    comment = fields.Text(string="Comment")

    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    writter = fields.Text(string="Writter", track_visibility='always')

    @api.model
    def create(self, vals):
        vals["writter"] = "Appointment scheduled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        return super(HospitalAppointment, self).create(vals)

