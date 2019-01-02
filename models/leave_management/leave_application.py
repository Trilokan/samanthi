# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Waiting For Approval'),
                 ('cancelled', 'Cancelled'),
                 ('approved', 'Approved')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Leave Application
class LeaveApplication(models.Model):
    _name = "leave.application"
    _inherit = "mail.thread"

    from_date = fields.Date(string="From Date", default=CURRENT_DATE, required=True)
    till_date = fields.Date(string="Till Date", default=CURRENT_DATE, required=True)
    person_id = fields.Many2one(comodel_name="lam.person", string="Employee",
                                default=lambda self: self.env.user.person_id.id,
                                readonly=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    writter = fields.Text(string="Writter", track_visibility="always")

    def check_month(self):
        attendance = self.env["time.attendance.detail"].search([("attendance_id.date", "=", self.from_date)])

        if attendance:
            if attendance.attendance_id.month_id.progress == "closed":
                raise exceptions.ValidationError("Error! Month is already closed")

    @api.multi
    def trigger_confirmed(self):
        self.check_month()
        writter = "Leave application confirmed by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "confirmed", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        self.check_month()
        writter = "Leave application cancelled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "cancelled", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        self.check_month()
        writter = "Leave application approved by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "approved", "writter": writter}

        self.write(data)

    @api.model
    def create(self, vals):
        self.check_month()
        vals["writter"] = "Leave application created by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        return super(LeaveApplication, self).create(vals)
