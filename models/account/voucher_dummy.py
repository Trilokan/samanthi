# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VoucherDummy(models.Model):
    _name = "voucher.dummy"

    voucher_id = fields.Many2one(comodel_name="hos.voucher", string="Voucher")
    item_id = fields.Many2one(comodel_name="journal.items", string="Amount")
    description = fields.Text(string="Description")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    reconcile_part_id = fields.Many2one(comodel_name="hos.reconcile", string="Reconcile")
    is_payment = fields.Boolean(string="Is Payment")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")

