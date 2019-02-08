# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# Work Detail
class WorkDetail(models.Model):
    _name = "work.detail"
    _inherit = "mail.thread"

    name = fields.Char(string="name")
    person_id = fields.Many2one(comodel_name="qin.person", string="Person")
    month_id = fields.Many2one(comodel_name="month.attendance", string="Month")
    total_days = fields.Float(string="Total Days")
    schedule_days = fields.Float(string="Scheduled Days")
    holidays = fields.Float(string="Holidays")
    holidays_present = fields.Float(string="Holiday Present")
    leave_taken = fields.Float(string="Leave Taken")
    permission_hours = fields.Float(string="Permission Hours")
    on_duty_hours = fields.Float(string="On-Duty Hours")
    lop_days = fields.Float(string="Loss Of Pay")

    leave_ids = fields.One2many(comodel_name="work.leave", inverse_name="work_id")
    # pay_ids = fields.One2many(comodel_name="work.pay", inverse_name="work_id")

    def check_month(self):
        if self.month_id.progress == "closed":
            raise exceptions.ValidationError("Error! Month is already closed")

    def clear_content(self):
        recs = self.leave_ids

        for rec in recs:
            rec.reconcile = 0
            rec.closing = 0

    def update_leave(self):
        config = self.env["leave.configuration"].search([("company_id", "=", self.env.user.company_id.id)])
        recs = self.env["work.leave"].search([("type_id", "!=", config.lop_id.id), ("work_id", "=", self.id)])

        leave_taken = self.leave_taken
        for rec in recs:
            total = (rec.opening + rec.credit) - rec.reconcile
            if leave_taken and total:
                if total >= leave_taken:
                    rec.reconcile = rec.reconcile + leave_taken
                    leave_taken = 0
                else:
                    rec.reconcile = rec.reconcile + total
                    leave_taken = leave_taken - total

        lop_rec = self.env["work.leave"].search([("type_id", "=", config.lop_id.id), ("work_id", "=", self.id)])
        lop_rec.reconcile = leave_taken

    def update_closing(self):
        config = self.env["leave.configuration"].search([("company_id", "=", self.env.user.company_id.id)])
        recs = self.env["work.leave"].search([("type_id", "!=", config.lop_id.id), ("work_id", "=", self.id)])

        for rec in recs:
            rec.closing = (rec.opening + rec.credit) - rec.reconcile

    def get_opening(self):
        start_date = self.month_id.start_date
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        actual_start_obj = start_date_obj - relativedelta(months=1)
        actual_end_obj = start_date_obj - timedelta(days=1)
        start = actual_start_obj.strftime("%Y-%m-%d")
        end = actual_end_obj.strftime("%Y-%m-%d")

        month_id = self.env["month.attendance"].search([("period_id.start_date", "=", start),
                                                        ("period_id.end_date", "=", end)])

        recs = self.env["work.leave"].search([("work_id", "=", self.id)])

        for rec in recs:
            work_obj = self.env["work.leave"].search([("type_id", "=", rec.type_id.id),
                                                      ("work_id.month_id", "=", month_id.id)])

            if work_obj:
                rec.opening = work_obj.closing

    def get_leave_level(self):
        recs = self.env["leave.level.item"].search([("level_id", "=", self.person_id.leave_level_id.id)])

        for rec in recs:
            leave_rec = self.env["work.leave"].search([("work_id", "=", self.id), ("type_id", "=", rec.type_id.id)])
            if not leave_rec:
                self.env["work.leave"].create({"type_id": rec.type_id.id,
                                               "work_id": self.id,
                                               "sequence": rec.sequence})

    @api.multi
    def update_leave_taken(self):
        self.check_month()
        self.clear_content()
        self.update_leave()
        self.update_closing()

    @api.multi
    def update_opening(self):
        self.get_leave_level()
        self.get_opening()

