# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomerPaymentDummy(models.Model):
    _name = "customer.payment.dummy"

    voucher_id = fields.Many2one(comodel_name="customer.payment", string="Voucher")
    item_id = fields.Many2one(comodel_name="journal.items", string="Amount")
    description = fields.Text(string="Description")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    reconcile_part_id = fields.Many2one(comodel_name="hos.reconcile", string="Reconcile")
    is_payment = fields.Boolean(string="Is Payment")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
