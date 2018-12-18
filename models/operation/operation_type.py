# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OperationType(models.Model):
    _name = "operation.type"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    procedure = fields.Html(string="Procedure", required=True)
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    total_operation = fields.Integer(string="Total Operation", compute="_get_total_operation")
    active = fields.Boolean(string="Active", default=True)

    def _get_total_operation(self):
        operation = self.env["hos.operation"].search_count([("type_id", "=", self.id),
                                                            ("progress", "=", "done")])
        self.total_operation = operation
