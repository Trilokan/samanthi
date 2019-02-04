# -*- coding: utf-8 -*-

from odoo import models, fields


# Leave Type
class LeaveType(models.Model):
    _name = "leave.type"

    name = fields.Char(string="Name", required=True)
    leave_type_uid = fields.Char(string="Code", required=True)
