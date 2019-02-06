# -*- coding: utf-8 -*-

from odoo import models, fields


# Leave Configuration
class LeaveConfiguration(models.Model):
    _name = "leave.configuration"

    lop_id = fields.Many2one(comodel_name="leave.type", string="Loss Of Pay")
    co_id = fields.Many2one(comodel_name="leave.type", string="Comp-Off")
