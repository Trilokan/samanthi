# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OperationTheater(models.Model):
    _name = "operation.theater"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    