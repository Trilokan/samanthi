# -*- coding: utf-8 -*-

from odoo import models, fields


class LeaveVoucherItem(models.Model):
    _name = "leave.voucher.item"

    type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type", required=True)
    opening = fields.Float(string="Opening", default=0.0, required=True)
    reconcile = fields.Float(string="Reconcile", default=0.0, required=True)
    closing = fields.Float(string="Closing", default=0.0, required=True)
    voucher_id = fields.Many2one(comodel_name="leave.voucher", string="Leave Voucher", required=True)
