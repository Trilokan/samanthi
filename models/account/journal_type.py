# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JournalType(models.Model):
    _name = "journal.type"

    name = fields.Char(string="Name", required=True)
    type_uid = fields.Char(string="Code", readonly=True)

    _sql_constraints = [("name", "unique(name)", "Journal Type must be unique"),
                        ("name", "unique(type_uid)", "Journal Type Code must be unique"),]

    @api.model
    def create(self, vals):
        vals["type_uid"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(JournalType, self).create(vals)
