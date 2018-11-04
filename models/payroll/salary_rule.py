# -*- coding: utf-8 -*-

from odoo import models, fields, api

RULE_TYPE = [("fixed", "Fixed"), ("formula", "Formula"), ("slab", "Slab")]


class SalaryRule(models.Model):
    _name = "salary.rule"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    rule_type = fields.Selection(selection=RULE_TYPE, string="Type")
