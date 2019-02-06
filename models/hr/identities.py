# -*- coding: utf-8 -*-

from odoo import models, fields


# Identity
class HRIdentity(models.Model):
    _name = "hr.identity"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    name = fields.Char(string="Identity", required=True)
    reference = fields.Char(string="Identity No", required=True)
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    _sql_constraints = [("name", "unique(name)", "Identity must be unique")]
