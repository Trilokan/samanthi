# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SchoolSection(models.Model):
    _name = "sch.section"
    _description = "School section masters"

    name = fields.Char(string="Section", required=True)
    code = fields.Char(string="Code", required=True)
    standard_id = fields.Many2one(comodel_name="sch.standard", string="Standard", required=True)
