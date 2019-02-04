# -*- coding: utf-8 -*-

from odoo import models, fields


class LeaveLevel(models.Model):
    _name = "leave.level"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    item_ids = fields.One2many(comodel_name="leave.level.item", inverse_name="level_id")

    _sql_constraints = [("code", "unique(code)", "Leave Level must be unique")]
