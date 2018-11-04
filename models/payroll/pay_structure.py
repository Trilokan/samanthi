# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class PayStructure(models.Model):
    _name = "pay.structure"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True)
    basic_pay = fields.Float(string="Basic", required=True)
    last_update_on = fields.Date(string="Last Updated On", required=True)
    structure_id = fields.Many2one(comodel_name="salary.structure", string="Salary Structure")
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position", required=True)
