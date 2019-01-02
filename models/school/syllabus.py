# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SchoolSyllabus(models.Model):
    _name = "sch.syllabus"
    _description = "School syllabus masters"

    name = fields.Char(string="Syllabus", required=True)
    code = fields.Char(string="Code", required=True)
    syllabus = fields.Html(string="Syllabus", required=True)
