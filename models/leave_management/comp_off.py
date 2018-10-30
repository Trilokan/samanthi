# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Waiting For Approval'),
                 ('cancelled', 'Cancelled'),
                 ('approved', 'Approved')]

DAY_TYPE = [('full_day', 'Full Day'), ('half_day', 'Half Day')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Comp-Off
class CompOffApplication(models.Model):
    _name = "compoff.application"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Employee",
                                default=lambda self: self.env.user.person_id.id,
                                readonly=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    co_type = fields.Selection(selection=DAY_TYPE, string="Type", default="full_day", required=True)

    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    writter = fields.Text(string="Writter", track_visibility="always")

    def check_month(self):
        attendance = self.env["time.attendance.detail"].search([("attendance_id.date", "=", self.date)])

        if attendance:
            if attendance.attendance_id.month_id.progress == "closed":
                raise exceptions.ValidationError("Error! Month is already closed")

    @api.multi
    def trigger_confirmed(self):
        self.check_month()
        writter = "Comp-Off application confirmed by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "confirmed", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        self.check_month()
        writter = "Comp-Off application cancelled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "cancelled", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        self.check_month()

        attendance = self.env["time.attendance.detail"].search([("attendance_id.date", "=", self.date)])
        employee_id = self.env["hr.employee"].search([("person_id", "=", self.person_id.id)])
        self.generate_journal(attendance, employee_id)

        writter = "Comp-Off application approved by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "approved", "writter": writter}

        self.write(data)

    @api.multi
    def generate_journal(self, attendance, employee):
        period_id = attendance.month_id.period_id

        leave_item = []

        if self.co_type == "full_day":
            value = 1
        elif self.co_type == "half_day":
            value = 0.5
        else:
            value = 0

        # Credit Detail - Employee
        journal_detail = {}
        journal_detail["period_id"] = period_id.id
        journal_detail["person_id"] = employee.person_id.id
        journal_detail["leave_account_id"] = employee.leave_account_id.id
        journal_detail["description"] = "Comp-Off Credit"
        journal_detail["debit"] = value
        journal_detail["reference"] = period_id.name

        leave_item.append((0, 0, journal_detail))

        # Credit Detail - Monthly
        journal_detail = {}
        journal_detail["period_id"] = period_id.id
        journal_detail["person_id"] = employee.person_id.id
        journal_detail["leave_account_id"] = self.env.user.company_id.leave_co_id.id
        journal_detail["description"] = "Comp-Off Credit"
        journal_detail["credit"] = value
        journal_detail["reference"] = period_id.name

        leave_item.append((0, 0, journal_detail))

        journal = {}
        journal["period_id"] = period_id.id
        journal["person_id"] = employee.person_id.id
        journal["journal_detail"] = leave_item
        journal["progress"] = "posted"
        journal["reference"] = period_id.name

        self.env["leave.journal"].create(journal)

    @api.model
    def create(self, vals):
        self.check_month()
        vals["writter"] = "Comp-Off application created by {0}".format(self.env.user.name)
        return super(CompOffApplication, self).create(vals)
