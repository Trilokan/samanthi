# -*- coding: utf-8 -*-

from odoo import models, fields


class HospitalWard(models.Model):
    _name = "hos.ward"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    supervisor_id = fields.Many2one(comodel_name="hos.person", string="Supervisor")
    bed_ids = fields.One2many(comodel_name="hos.bed", inverse_name="ward_id", string="Bed")
    comment = fields.Text(string="Comment")
