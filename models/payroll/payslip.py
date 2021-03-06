# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'), ('generated', 'Generated')]
PAY_TYPE = [('allowance', 'Allowance'), ('deduction', 'Deduction')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Payslip
class Payslip(models.Model):
    _name = "pay.slip"
    _inherit = "mail.thread"
    _rec_name = "employee_id"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", readonly=True)
    month_id = fields.Many2one(comodel_name="month.attendance", string="Month", readonly=True)
    payslip_details = fields.One2many(comodel_name="payslip.detail", inverse_name="payslip_id")
    total_days = fields.Float(string="Total Days", readonly=True)
    schedule_days = fields.Float(string="Scheduled Days", readonly=True)
    lop_days = fields.Float(string="Lop Days", readonly=True)
    present_days = fields.Float(string="Present Days", readonly=True)
    absent_days = fields.Float(string="Absent Days", readonly=True)
    total_holidays = fields.Float(string="Total Holidays", readonly=True)
    holiday_present = fields.Float(string="Holiday Present", readonly=True)
    payslip_report = fields.Html(string="Payslip Report", readonly=True)
    writter = fields.Text(string="Writter", track_visibility='always')
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

    _sql_constraints = [('payslip_uniq', 'unique(employee_id, month_id)', 'Payslip is already generated')]

    def check_items(self):
        conf = self.env["leave.configuration"].search([("company_id", "=", self.env.user.company_id.id)])

        hr_pay = self.env["hr.pay"].search([("employee_id", "=", self.employee_id.id)])
        lop = self.env["leave.journal.item"].search([("person_id", "=", self.employee_id.person_id.id),
                                                     ("entry_id.period_id", "=", self.month_id.period_id.id),
                                                     ("account_id", "=", conf.lop_id.id)])

        if not hr_pay:
            raise exceptions.ValidationError("Error! Pay details is not configured")

        if self.month_id.progress != "closed":
            raise exceptions.ValidationError("Error! Monthly attendance is not closed")

        if not lop:
            raise exceptions.ValidationError("Error! LOP is not calculated")

    @api.multi
    def generate_payslip(self):
        self.check_items()
        self.payslip_details.unlink()

        pay = self.update_payslip_dict()

        hr_pay = self.env["hr.pay"].search([("employee_id", "=", self.employee_id.id)])

        recs = hr_pay.structure_id.detail_ids
        sorted(recs, key=lambda x: x.sequence)

        person = self.employee_id.person_id
        self.total_days = self.month_id.get_days_in_month()
        self.schedule_days = self.month_id.get_total_days(person)
        self.present_days = self.month_id.get_present_days(person)
        self.absent_days = self.month_id.get_absent_days(person)
        self.total_holidays = self.month_id.get_holidays(person)
        self.holiday_present = self.month_id.get_holidays_present(person)
        self.lop_days = self.month_id.get_lop_days(person)

        for rec in recs:
            if rec.is_need:
                data = {"code": rec.rule_id.code.id,
                        "unit_price": pay[rec.rule_id.code.name],
                        "payslip_id": self.id,
                        "pay_order": rec.sequence,
                        "pay_type": rec.pay_type}
                payslip_detail = self.env["payslip.detail"].create(data)
                payslip_detail.calculate_amount()

        writter = "Payslip is generated by {0}".format(self.env.user.name)
        self.write({"progress": "generated", "writter": writter})

    @api.multi
    def update_payslip_dict(self):
        hr_pay = self.env["hr.pay"].search([("employee_id", "=", self.employee_id.id)])
        recs = hr_pay.structure_id.detail_ids
        sorted(recs, key=lambda x: x.sequence)

        pay = {"BASIC": hr_pay.basic}

        for rec in recs:
            if rec.rule_id.rule_type == "fixed":
                pay[rec.rule_id.code.name] = rec.rule_id.fixed

            elif rec.rule_id.rule_type == "formula":
                pay[rec.rule_id.code.name] = eval(rec.rule_id.formula, pay)

            elif rec.rule_id.rule_type == "slab":
                for record in rec.rule_id.slab_ids:
                    if record.range_till >= eval(record.slab_input, pay) >= record.range_from:
                        if record.slab_type == "fixed":
                            pay[rec.rule_id.code.name] = record.fixed
                        elif record.slab_type == "formula":
                            pay[rec.rule_id.code.name] = eval(record.formula, pay)
                        else:
                            pay[rec.rule_id.code.name] = 0
                    else:
                        pay[rec.rule_id.code.name] = 0
        return pay


class PayslipDetail(models.Model):
    _name = "payslip.detail"

    code = fields.Many2one(comodel_name="salary.rule.code", string="Code", readonly=True)
    unit_price = fields.Float(string="Unit Price", readonly=True)
    amount = fields.Float(string="Amount", readonly=True)
    pay_order = fields.Integer(string="Pay Order", readonly=True)
    pay_type = fields.Selection(PAY_TYPE, string='Pay Type', readonly=True)
    payslip_id = fields.Many2one(comodel_name="pay.slip", string="payslip")

    def calculate_amount(self):
        unit_price = self.unit_price / 30
        amount = (unit_price * self.payslip_id.schedule_days) - (unit_price * self.payslip_id.lop_days)
        self.write({"amount": amount})

    _sql_constraints = [('salary_details_uniq', 'unique(code, payslip_id)', 'Salary details should not duplicated')]

