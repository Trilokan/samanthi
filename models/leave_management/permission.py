# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Waiting For Approval'),
                 ('cancelled', 'Cancelled'),
                 ('approved', 'Approved')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class PermissionApplication(models.Model):
    _name = "permission.application"

    date = fields.Date(string="Date", default=CURRENT_TIME, required=True)
    from_time = fields.Float(string="From Time", default=0.0, required=True)
    till_time = fields.Float(string="Till Time", default=0.0, required=True)
    person_id = fields.Many2one(comodel_name="qin.person", string="Person", required=True)
    reason = fields.Text(string="Reason")
    total_hours = fields.Float(string="Total Hours", default=0.0, required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def check_month(self):
        from_date_obj = datetime.strptime(self.from_time, "%Y-%m-%d %H:%M:%S")
        from_date = from_date_obj.strftime("%Y-%m-%d")
        attendance = self.env["employee.attendance"].search([("attendance_id.date", "=", from_date)])

        if attendance:
            if attendance.attendance_id.month_id.progress == "closed":
                raise exceptions.ValidationError("Error! Month is already closed")

    def update_total_hours(self):
        from_time_obj = datetime.strptime(self.from_time, "%Y-%m-%d %H:%M:%S")
        till_time_obj = datetime.strptime(self.till_time, "%Y-%m-%d %H:%M:%S")

        secs = (till_time_obj - from_time_obj).seconds
        minutes = ((secs / 60) % 60) / 60.0
        hours = secs / 3600

        return hours + minutes

    @api.multi
    def trigger_confirmed(self):
        self.check_month()
        writter = "Permission confirmed by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "confirmed",
                "total_hours": self.update_total_hours(),
                "writter": writter}

        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        self.check_month()
        writter = "Permission cancelled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "cancelled", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        self.check_month()
        writter = "Permission approved by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "approved", "writter": writter}

        self.write(data)

    @api.model
    def create(self, vals):
        self.check_month()
        vals["writter"] = "Permission created by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        return super(PermissionApplication, self).create(vals)
