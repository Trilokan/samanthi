# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VoucherDummy(models.Model):
    _name = "voucher.dummy"

    amount = fields.Float(string="Amount")
    item_id = fields.Many2one(comodel_name="journal.items", string="Amount")
    reconcile = fields.Boolean(string="Reconcile")
    voucher_id = fields.Many2one(comodel_name="hos.voucher", string="Voucher")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    reconcile_part_id = fields.Many2one(comodel_name="hos.reconcile", string="Reconcile")
