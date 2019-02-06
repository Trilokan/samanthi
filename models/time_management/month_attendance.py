# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime, timedelta
from calendar import monthrange

PROGRESS_INFO = [('draft', 'draft'), ('open', 'Open'), ('closed', 'Closed')]


# Month Attendance
class MonthAttendance(models.Model):
    _name = "month.attendance"
    _rec_name = "period_id"

    period_id = fields.Many2one(comodel_name="qin.period", string="Month", required=True)
    month_detail = fields.One2many(comodel_name="daily.attendance", inverse_name="month_id")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', default="draft")

    _sql_constraints = [('unique_period_id', 'unique (period_id)', 'Error! Month must be unique')]

    def get_days_in_month(self):
        from_date = self.period_id.from_date
        till_date = self.period_id.till_date

        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
        till_date_obj = datetime.strptime(till_date, "%Y-%m-%d")

        return (till_date_obj - from_date_obj).days + 1

    def get_total_days(self, person):
        total_days = self.env["employee.attendance"].search_count([("person_id", "=", person.id),
                                                                   ("attendance_id.month_id", "=", self.id),
                                                                   ("day_progress", "in", ["working_day", "holiday"])])

        return total_days

    def get_present_days(self, person):
        full_day = self.env["employee.attendance"].search_count([("person_id", "=", person.id),
                                                                 ("attendance_id.month_id", "=", self.id),
                                                                 ("availability_progress", "=", "full_day")])

        half_day = self.env["employee.attendance"].search_count([("person_id", "=", person.id),
                                                                 ("attendance_id.month_id", "=", self.id),
                                                                 ("availability_progress", "=", "half_day")])

        return full_day + (0.5 * half_day)

    def get_absent_days(self, person):
        absent = self.env["employee.attendance"].search_count([("person_id", "=", person.id),
                                                               ("attendance_id.month_id", "=", self.id),
                                                               ("day_progress", "=", "working_day"),
                                                               ("availability_progress", "=", "absent")])

        half_day = self.env["employee.attendance"].search_count([("person_id", "=", person.id),
                                                                 ("attendance_id.month_id", "=", self.id),
                                                                 ("day_progress", "=", "working_day"),
                                                                 ("availability_progress", "=", "half_day")])

        return absent + (0.5 * half_day)

    def get_working_days(self, person):
        working_day = self.env["employee.attendance"].search_count([("person_id", "=", person.id),
                                                                    ("attendance_id.month_id", "=", self.id),
                                                                    ("day_progress", "=", "working_day")])

        return working_day

    def get_holidays(self, person):
        holiday = self.env["employee.attendance"].search_count([("person_id", "=", person.id),
                                                                ("attendance_id.month_id", "=", self.id),
                                                                ("day_progress", "=", "holiday")])

        return holiday

    def get_holidays_present(self, person):
        full_day = self.env["employee.attendance"].search_count([("person_id", "=", person.id),
                                                                 ("attendance_id.month_id", "=", self.id),
                                                                 ("day_progress", "=", "holiday"),
                                                                 ("availability_progress", "=", "full_day")])

        half_day = self.env["employee.attendance"].search_count([("person_id", "=", person.id),
                                                                 ("attendance_id.month_id", "=", self.id),
                                                                 ("day_progress", "=", "holiday"),
                                                                 ("availability_progress", "=", "half_day")])

        return full_day + (0.5 * half_day)

    def get_lop_days(self, person):
        conf = self.env["leave.configuration"].search([("company_id", "=", self.env.user.company_id.id)])
        rec = self.env["leave.journal.item"].search([("entry_id.period_id", "=", self.period_id.id),
                                                     ("person_id", "=", person.id),
                                                     ("account_id", "=", conf.lop_id.id)])

        if len(rec) != 1:
            raise exceptions.ValidationError("Error! Multiple LOP in a month")

        return rec.debit

    def get_leave_available(self, person):
        employee_id = self.env["hr.employee"].search([("person_id", "=", person.id)])
        leave_account_id = employee_id.leave_account_id.id
        recs = self.env["leave.item"].search([("leave_account_id", "=", leave_account_id),
                                              ("debit", ">", 0),
                                              ("reconcile_id", "=", False)])

        available = 0
        for rec in recs:
            available = available + rec.debit

        return available

    def generate_header(self, date_list):
        top_header = """
                        <tr>
                            <th colspan="{0}">
                                <h1>Monthly Attendance</h1>                                
                            </th>
                        </tr>
                        <tr>{1}</tr>
                     """

        header = ""

        header_list = ["Employee"] + date_list + ["Total Days",
                                                  "Present Days",
                                                  "Absent Days",
                                                  "Holidays",
                                                  "Holidays Present"]

        for rec in header_list:
            header = "{0}\n<th>{1}</th>".format(header, rec)

        return top_header.format(len(header_list), header)

    def generate_body(self, date_list, person_list):
        body = ""

        for person in person_list:
            person_id = self.env["qin.person"].search([("id", "=", person)])
            body = "{0}\n<tr><td>{1}</td>".format(body, person_id.name)

            for date in date_list:
                attendance = self.env["employee.attendance"].search([("person_id", "=", person),
                                                                     ("attendance_id.date", "=", date)])
                body = "{0}\n<td>{1}</td>".format(body, attendance.availability_progress)

            total_days = self.get_total_days(person_id)
            present_days = self.get_present_days(person_id)
            absent_days = self.get_absent_days(person_id)
            holidays = self.get_holidays(person_id)
            holiday_present = self.get_holidays_present(person_id)

            body = """{0}<td>{1}</td>
                         <td>{2}</td>
                         <td>{3}</td>
                         <td>{4}</td>
                         <td>{5}</td></tr>""".format(body,
                                                     total_days,
                                                     present_days,
                                                     absent_days,
                                                     holidays,
                                                     holiday_present)

        return body

    def trigger_preview(self):
        recs = self.month_detail

        date_list = []
        person_list = []
        for rec in recs:
            date_list.append(rec.date)

        recs = self.env["employee.attendance"].search([("attendance_id.month_id", "=", self.id)])

        for rec in recs:
            if rec.person_id.id not in person_list:
                person_list.append(rec.person_id.id)

        header = self.generate_header(date_list)
        body = self.generate_body(date_list, person_list)

        html = self.env.user.company_id.template_attendance
        report = html.format(header, body)

        view = self.env.ref('nagini.view_month_attendance_wiz_form')

        return {
            'name': 'Monthly Attendance',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'month.attendance.wiz',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'report': report}
        }

    def check_attendance(self):
        draft = self.env["time.attendance"].search_count([("month_id", "=", self.id), ("progress", "!=", "verified")])

        if draft:
            raise exceptions.ValidationError("Error! Daily attendance report is not verified")

        date = datetime.strptime(self.period_id.from_date, "%Y-%m-%d")

        _, num_days = monthrange(date.year, date.month)
        attendance = self.env["time.attendance"].search_count([("month_id", "=", self.id), ("progress", "=", "verified")])

        if num_days != attendance:
            raise exceptions.ValidationError("Error! {0} Days missing in attendance".format(num_days - attendance))

    @api.multi
    def trigger_closed(self):
        self.check_attendance()
        employees = self.env["hr.employee"].search([])

        for employee in employees:
            total_absent = self.get_absent_days(employee.person_id)

            voucher = {"period_id": self.period_id.id,
                       "person_id": employee.person_id.id,
                       "month_id": self.id,
                       "leave_taken": total_absent}

            voucher_id = self.env["leave.voucher"].create(voucher)
            voucher_id.trigger_recon()

        self.write({"progress": "closed"})

    def generate_journal_entries(self, period_id, employee):
        levels = self.env["leave.level.detail"].search([("level_id", "=", employee.leave_level_id.id)])

        # Credit Detail - Employee
        leave_item = []
        for level in levels:
            # Leave Journal Credit
            journal_credit = {"person_id": employee.person_id.id,
                              "description": "{0} Leave Credit".format(level.type_id.name),
                              "credit": level.credit,
                              "type_id": level.type_id.id,
                              "priority": level.sequence,
                              "account_id": employee.leave_account_id.id}

            leave_item.append((0, 0, journal_credit))

            # Leave Journal Debit
            journal_debit = {"person_id": employee.person_id.id,
                             "description": "{0} Leave Credit".format(level.type_id.name),
                             "debit": level.credit,
                             "type_id": level.type_id.id,
                             "priority": level.sequence,
                             "account_id": level.type_id.account_id.id}

            leave_item.append((0, 0, journal_debit))

        if leave_item:
            journal_entry = {"period_id": period_id.id,
                             "journal_item": leave_item,
                             "progress": "posted"}

            self.env["leave.journal.entry"].create(journal_entry)

    @api.multi
    def trigger_open(self):
        if self.env["month.attendance"].search_count([("progress", "=", "open"), ("id", "!=", self.id)]):
            raise exceptions.ValidationError("Error! Please close all open months before open")

        # Leave Credits from leave configuration
        employees = self.env["hr.employee"].search([("leave_level_id", "!=", False)])

        for employee in employees:
            self.generate_journal_entries(self.period_id, employee)

        self.write({"progress": "open"})
