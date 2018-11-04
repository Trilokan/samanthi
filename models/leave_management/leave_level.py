# -*- coding: utf-8 -*-

from odoo import models, fields


class LeaveLevel(models.Model):
    _name = "leave.level"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    _sql_constraints = [
        ("code", "unique(code)", "Leave Level must be unique"),
    ]


