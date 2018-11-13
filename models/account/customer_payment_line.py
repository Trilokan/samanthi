# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomerPaymentLine(models.Model):
    _name = "customer.payment.line"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    total_amount = fields.Float(string="Total Amount", default=0)
    opening_amount = fields.Float(string="Opening", default=0)
    reconcile_amount = fields.Float(string="Reconcile")
    credit_id = fields.Many2one(comodel_name="customer.payment", string="Credit")
    debit_id = fields.Many2one(comodel_name="customer.payment", string="Debit")
    reconcile = fields.Boolean(string="Reconcile")
    reconcile_part_id = fields.Many2one(comodel_name="hos.reconcile", string="Partial Reconcile")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    item_id = fields.Many2one(comodel_name="journal.items", string="Journal Items")
