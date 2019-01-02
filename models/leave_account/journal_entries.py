# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveJournalEntry(models.Model):
    _name = "leave.journal.entry"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    period_id = fields.Many2one(comodel_name="period.period", string="Period", required=True)
    journal_item = fields.One2many(comodel_name="leave.journal.item", inverse_name="entry_id", string="Journal Item")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(LeaveJournalEntry, self).create(vals)


class LeaveJournalItem(models.Model):
    _name = "leave.journal.item"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="lam.person", string="Person", required=True)
    account_id = fields.Many2one(comodel_name="leave.account", string="Account", required=True)
    type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    description = fields.Text(string="Description")
    credit = fields.Float(string="Credit", default=0, required=True)
    debit = fields.Float(string="Debit", default=0, required=True)
    reconcile_id = fields.Many2one(comodel_name="leave.reconcile", string="Reconcile", required=False)
    part_reconcile_id = fields.Many2one(comodel_name="leave.reconcile", string="Partial Reconcile")
    priority = fields.Integer(string="Priority", default=0)
    entry_id = fields.Many2one(comodel_name="leave.journal.entry", string="Entry")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="entry_id.progress")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(LeaveJournalItem, self).create(vals)
