# -*- coding: utf-8 -*-

from odoo import models, fields


# Language
class Language(models.Model):
    _name = "lam.language"

    name = fields.Char(string="Language", required=True)

