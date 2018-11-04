# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalWard(models.Model):
    _name = "hos.ward"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    bed_ids = fields.One2many(comodel_name="hos.bed", inverse_name="ward_id", string="Bed")
