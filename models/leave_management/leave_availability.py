# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveAvailability(models.TransientModel):
    _name = "leave.availability"

    person_id = fields.Many2one(comodel_name="hos.person", string="Employee")
    leave_detail = fields.One2many(comodel_name="leave.availability.detail", inverse_name="available_id")

    @api.onchange("person_id")
    def onchange_person_id(self):
        if self.person_id.id:
            employee_id = self.env["hr.employee"].search([("person_id", "=", self.person_id.id)])
            account_id = employee_id.leave_account_id.id

            availability = []
            type_ids = self.env["leave.type"].search([])
            for type_id in type_ids:
                recs = self.env["leave.journal.item"].search([("account_id", "=", account_id),
                                                              ("reconcile_id", "=", False),
                                                              ("credit", ">", 0),
                                                              ("type_id", "=", type_id.id)])

                total = 0
                for rec in recs:
                    total = total + rec.credit

                    if rec.part_reconcile_id:
                        items = self.env["leave.journal.item"].search([("part_reconcile_id", "=", rec.part_reconcile_id.id)])
                        total = total - sum(items.mapped('debit'))

                availability.append((0, 0, {"type_id": type_id.id, "available": total}))

            self.leave_detail = availability


class LeaveAvailabilityDetail(models.TransientModel):
    _name = "leave.availability.detail"

    available_id = fields.Many2one(comodel_name="leave.availability", string="Leave Type")
    type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    available = fields.Float(string="Available")
