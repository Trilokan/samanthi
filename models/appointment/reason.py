# -*- coding: utf-8 -*-

from odoo import models, fields


class AppointmentReason(models.Model):
    _name = "appointment.reason"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

