# -*- coding: utf-8 -*-

from odoo import models, fields


class LeaveVoucher(models.Model):
    _name = "leave.voucher"

    period_id = fields.Many2one(comodel_name="qin.period", string="Period", required=True)
    person_id = fields.Many2one(comodel_name="qin.person", string="Person", required=True)
    item_ids = fields.One2many(comodel_name="leave.voucher.item", inverse_name="voucher_id")
