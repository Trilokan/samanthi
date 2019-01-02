# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AcademicSection(models.Model):
    _name = "aca.section"

    section_id = fields.Many2one(comodel_name="sch.section", string="Section", required=True)
    standard_id = fields.Many2one(comodel_name="sch.standard", string="Standard", required=True)

    student_ids = fields.One2many(comodel_name="sch.student", inverse_name="section_id")
    # subject_ids = fields.One2many(comodel_name="aca.subject", inverse_name="section_id")
    supervisor_id = fields.Many2one(comodel_name="lam.person", string="")

