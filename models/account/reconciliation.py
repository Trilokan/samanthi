# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Reconciliation(models.Model):
    _name = "hos.reconciliation"

    name = fields.Char(string="Name")

