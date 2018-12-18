# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime

APPOINTMENT_TYPE = [("opt", "OPT"), ("ot", "OT"), ("meeting", "Meeting")]

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Appointment
class Appointment(models.TransientModel):
    _name = "hos.appointment"

    employee_id = fields.Many2one(comodel_name="hos.person", string="Doctor/ Employee")
    patient_id = fields.Many2one(comodel_name="hos.person", string="Person")
    appointment_ids = fields.One2many(comodel_name="hos.appointment.detail", inverse_name="appointment_id")

    @api.onchange("employee_id")
    def get_doctor_appointment(self):
        if self.employee_id:
            self.appointment_ids.unlink()
            detail = []

            # Out-Patient
            recs = self.env["appointment.opt"].search([("employee_id", "=", self.employee_id.id)])

            for rec in recs:
                detail.append((0, 0, rec.copy_data()[0]))

            # Meeting
            recs = self.env["appointment.opt"].search([("employee_id", "=", self.employee_id.id)])

            for rec in recs:
                detail.append((0, 0, rec.copy_data()[0]))

            self.appointment_ids = detail

            # Operation Theater


class AppointmentDetail(models.TransientModel):
    _name = "hos.appointment.detail"

    date = fields.Datetime(string="Date", default=CURRENT_TIME, required=True)
    employee_id = fields.Many2one(comodel_name="hos.person", string="Doctor")
    patient_id = fields.Many2one(comodel_name="hos.person", string="Person")
    reason = fields.Many2one(comodel_name="appointment.reason", string="Reason")
    comment = fields.Text(string="Comment")
    appointment_id = fields.Many2one(comodel_name="hos.appointment", string="Appointment")

