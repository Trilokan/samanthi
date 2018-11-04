# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalaryStructure(models.Model):
    _name = "salary.structure"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    rule_ids = fields.One2many(comodel_name="salary.rule", inverse_name="structure_id", string="Salary Rule")
