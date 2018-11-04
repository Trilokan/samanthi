# -*- coding: utf-8 -*-

from odoo import models, fields


class LeaveType(models.Model):
    _name = "leave.type"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    _sql_constraints = [
        ("code", "unique(code)", "Leave Type must be unique"),
    ]


