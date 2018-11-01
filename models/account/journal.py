# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Journal(models.Model):
    _name = "hos.journal"

    name = fields.Char(string="Name")
    code = fields.Char(sring="Code")
