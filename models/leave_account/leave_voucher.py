# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("posted", "Posted")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveVoucher(models.Model):
    _name = "leave.voucher"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    month_id = fields.Many2one(comodel_name="month.attendance", string="Month", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    voucher_detail = fields.One2many(comodel_name="leave.voucher.detail", inverse_name="voucher_id")
    voucher_dummy = fields.One2many(comodel_name="leave.voucher.dummy", inverse_name="voucher_id")
    leave_taken = fields.Float(string="Leave Taken", default=0, required=True)
    lop = fields.Float(string="Loss Of Pay", default=0, required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    entry_id = fields.Many2one(comodel_name="leave.journal.entry", string="Journal Entry")

    def reconciliation(self):
        pass

    def get_leave_journal_items(self):
        pass

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(LeaveVoucher, self).create(vals)


