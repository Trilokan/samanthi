# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SchoolStandard(models.Model):
    _name = "sch.standard"
    _description = "School standards masters"

    name = fields.Char(string="Standard", required=True)
    code = fields.Char(string="Code", required=True)

