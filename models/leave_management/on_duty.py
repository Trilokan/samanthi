# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Waiting For Approval'),
                 ('cancelled', 'Cancelled'),
                 ('approved', 'Approved')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class OnDutyApplication(models.Model):
    _name = "on.duty.application"

    from_date = fields.Date(string="From Date", default=CURRENT_DATE, required=True)
    till_date = fields.Date(string="Till Date", default=CURRENT_DATE, required=True)
    person_id = fields.Many2one(comodel_name="qin.person", string="Person", required=True)
    reason = fields.Text(string="Reason")
    total_days = fields.Float(string="Total Days", default=0.0, readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def check_month(self):
        attendance = self.env["employee.attendance"].search([("attendance_id.date", "=", self.date)])

        if attendance:
            if attendance.attendance_id.month_id.progress == "closed":
                raise exceptions.ValidationError("Error! Month is already closed")

    @api.multi
    def trigger_confirmed(self):
        self.check_month()
        writter = "On-Duty application confirmed by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "confirmed", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        self.check_month()
        writter = "On-Duty application cancelled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "cancelled", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        self.check_month()
        writter = "On-Duty application approved by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "approved", "writter": writter}

        self.write(data)

    @api.model
    def create(self, vals):
        self.check_month()
        vals["writter"] = "On-Duty application created by {0}".format(self.env.user.name)
        return super(OnDutyApplication, self).create(vals)
