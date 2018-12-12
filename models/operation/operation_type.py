# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OperationType(models.Model):
    _name = "operation.type"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    procedure = fields.Html(string="Procedure", required=True)
    active = fields.Boolean(string="Active", default=True)
