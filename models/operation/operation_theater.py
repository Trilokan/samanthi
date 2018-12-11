# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OperationTheater(models.Model):
    _name = "operation.theater"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    _sql_constraints = [("name", "unique(name)", "Operation Theater must be unique"),
                        ("code", "unique(code)", "Operation Theater must be unique")]
