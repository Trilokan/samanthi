# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QinAccount(models.Model):
    _name = "qin.account"

    name = fields.Char(string="Name", required=True)
    account_uid = fields.Char(string="Code", readonly=True)
    person_id = fields.Many2one(comodel_name="qin.person", string="Person")

    @api.model
    def create(self, vals):
        vals["account_uid"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(QinAccount, self).create(vals)
