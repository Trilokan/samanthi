# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AcademicStandard(models.Model):
    _name = "academic.standard"

    standard_id = fields.Many2one(comodel_name="sch.standard", string="Standard")
    section_ids = fields.One2many(comodel_name="academic.section", inverse_name="standard_id")

