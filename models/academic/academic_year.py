# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .. import calculation as cal


class AcademicYear(models.Model):
    _name = "academic.year"
    _description = "Academic Year settings"

    name = fields.Char(string="Academic Year", readonly=True)
    year = fields.Selection(selection=cal.get_list_year(), string="Year", required=True)


