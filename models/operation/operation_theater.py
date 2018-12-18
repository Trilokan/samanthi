# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OperationTheater(models.Model):
    _name = "operation.theater"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    description = fields.Text(sring="Description")
    length = fields.Float(string="Length")
    breadth = fields.Float(string="Breadth")
    area = fields.Float(string="Area")
    equipment_ids = fields.Many2many(comodel_name="hos.asserts", sytring="Equipments")
    incharge_id = fields.Many2one(comodel_name="hos.person", string="In-Charge")
    total_operation = fields.Integer(string="Total Operation", compute="_get_total_operation")
    in_progress_operation = fields.Integer(string="In Progress", compute="_get_in_progress_operation")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    _sql_constraints = [("name", "unique(name)", "Operation Theater must be unique"),
                        ("code", "unique(code)", "Operation Theater must be unique")]

    def _get_total_operation(self):
        operation = self.env["hos.operation"].search_count([("theater_id", "=", self.id),
                                                            ("progress", "=", "done")])
        self.total_operation = operation

    def _get_in_progress_operation(self):
        operation = self.env["hos.operation"].search_count([("theater_id", "=", self.id),
                                                            ("progress", "=", "scheduled")])
        self.in_progress_operation = operation
