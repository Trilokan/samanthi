# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]
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
    account_id = fields.Many2one(comodel_name="leave.account", string="Account")
    entry_id = fields.Many2one(comodel_name="leave.journal.entry", string="Entry")

    _sql_constraints = [("month", "unique(month_id, person_id)", "Leave duplicates not allowed")]

    def reconciliation(self, credits, leave_taken):
        for rec in credits:
            balance = rec.available - rec.opening

            if balance and leave_taken:
                if not rec.part_reconcile_id:
                    part_reconcile_id = self.env["leave.reconcile"].create({})
                    rec.part_reconcile_id = part_reconcile_id.id

                if leave_taken > balance:
                    rec.reconcile = rec.opening + balance
                    leave_taken = leave_taken - balance

                    data = {"date": rec.date,
                            "person_id": rec.person_id.id,
                            "account_id": rec.account_id.id,
                            "description": rec.description,
                            "debit": balance,
                            "part_reconcile_id": rec.part_reconcile_id.id,
                            "voucher_id": self.id}

                    self.env["leave.voucher.dummy"].create(data)

                else:
                    rec.reconcile = rec.opening + leave_taken

                    data = {"date": rec.date,
                            "person_id": rec.person_id.id,
                            "account_id": rec.account_id.id,
                            "description": rec.description,
                            "debit": leave_taken,
                            "part_reconcile_id": rec.part_reconcile_id.id,
                            "voucher_id": self.id}

                    self.env["leave.voucher.dummy"].create(data)
                    leave_taken = 0

        return leave_taken

    def leave_reconcile(self):
        config = self.env["leave.configuration"].search([("company_id", "=", self.env.user.company_id.id)])
        employee_id = self.env["hr.employee"].search([("person_id", "=", self.person_id.id)])
        self.account_id = employee_id.leave_account_id.id

        voucher_detail = self.voucher_detail
        leave_taken = self.leave_taken

        data = {"date": self.date,
                "person_id": self.person_id.id,
                "account_id": config.account_id.id,
                "description": "Leave Taken for {0}".format(self.month_id.period_id.name),
                "credit": leave_taken,
                "voucher_id": self.id}

        self.env["leave.voucher.dummy"].create(data)

        reconcile = self.reconciliation(voucher_detail, leave_taken)

        if reconcile:
            data = {"date": self.date,
                    "person_id": self.person_id.id,
                    "account_id": config.lop_id.id,
                    "description": "Loss Of Pay for {0}".format(self.month_id.period_id.name),
                    "debit": reconcile,
                    "voucher_id": self.id}

            self.env["leave.voucher.dummy"].create(data)
            self.lop = reconcile

    def get_leave_journal_items(self):
        employee_id = self.env["hr.employee"].search([("person_id", "=", self.person_id.id)])
        account_id = employee_id.leave_account_id.id

        debit = []
        recs = self.env["leave.journal.item"].search([("account_id", "=", account_id),
                                                      ("reconcile_id", "=", False),
                                                      ("credit", ">", 0)])

        for rec in recs:
            data = {"date": rec.date,
                    "name": rec.name,
                    "account_id": rec.account_id.id,
                    "person_id": rec.person_id.id,
                    "description": rec.description,
                    "available": rec.credit,
                    "opening": 0,
                    "item_id": rec.id}

            if rec.part_reconcile_id:
                items = self.env["leave.journal.item"].search([("part_reconcile_id", "=", rec.part_reconcile_id.id)])
                data["opening"] = sum(items.mapped('debit'))
                data["part_reconcile_id"] = rec.part_reconcile_id.id

            if data["available"] < data["opening"]:
                raise exceptions.ValidationError("Error! Please check leave reconcilation")

            debit.append((0, 0, data))

        self.voucher_detail = debit

    def generate_leave_journals(self):
        recs = self.env["leave.voucher.dummy"].search([("voucher_id", "=", self.id)])

        item = []
        for rec in recs:
            data = {"date": rec.date,
                    "account_id": rec.account_id.id,
                    "person_id": rec.person_id.id,
                    "description": rec.description,
                    "period_id": self.month_id.period_id.id,
                    "credit": rec.credit,
                    "debit": rec.debit,
                    "part_reconcile_id": rec.part_reconcile_id.id}

            item.append((0, 0, data))

        entry_id = self.env["leave.journal.entry"].create({"period_id": self.month_id.period_id.id,
                                                           "journal_item": item})
        self.entry_id = entry_id.id

    @api.multi
    def update_reconciliation(self):
        for rec in self.voucher_detail:
            rec.item_id.part_reconcile_id = rec.part_reconcile_id.id
            self.env["leave.reconcile"].check_reconciliation(rec.part_reconcile_id.id)

    @api.multi
    def trigger_recon(self):
        self.voucher_detail.unlink()
        self.voucher_dummy.unlink()
        self.get_leave_journal_items()
        self.leave_reconcile()
        self.generate_leave_journals()
        self.update_reconciliation()
        self.write({"progress": "posted"})

    def trigger_cancel(self):

        self.write({"progress": "cancel"})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(LeaveVoucher, self).create(vals)


