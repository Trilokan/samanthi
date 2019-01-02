# -*- coding: utf-8 -*-

from odoo import models, fields


# Religion
class Religion(models.Model):
    _name = "lam.religion"

    name = fields.Char(string="Religion", required=True)
