# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveReconcile(models.Model):
    _name = "leave.reconcile"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    part_reconcile_ids = fields.One2many(comodel_name="leave.journal.item", inverse_name="part_reconcile_id", string="Partial Reconcile")
    reconcile_ids = fields.One2many(comodel_name="leave.journal.item", inverse_name="reconcile_id", string="Fully Reconcile")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(LeaveReconcile, self).create(vals)
