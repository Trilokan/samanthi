# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalBed(models.Model):
    _name = "hos.bed"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    ward_id = fields.Many2one(comodel_name="hos.ward", string="Ward")
