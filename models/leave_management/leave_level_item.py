# -*- coding: utf-8 -*-

from odoo import models, fields


class LeaveLevelItem(models.Model):
    _name = "leave.level.item"

    sequence = fields.Integer(string="Sequence")
    type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type", required=True)
    credit = fields.Float(string="Leave Credit", default=0.0, required=True)
    level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level", required=True)
