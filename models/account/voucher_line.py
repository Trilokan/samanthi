# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VoucherLine(models.Model):
    _name = "voucher.line"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    total_amount = fields.Float(string="Total Amount")
    opening_amount = fields.Float(string="Opening")
    reconcile_amount = fields.Float(string="Reconcile")
    credit_id = fields.Many2one(comodel_name="hos.voucher", string="Credit")
    debit_id = fields.Many2one(comodel_name="hos.voucher", string="Debit")
    reconcile = fields.Boolean(string="Reconcile")
    reconcile_part_id = fields.Many2one(comodel_name="hos.reconciliation", string="Partial Reconcile")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    item_id = fields.Many2one(comodel_name="journal.items", string="Journal Items")
