# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Account(models.Model):
    _name = "hos.account"

    name = fields.Char(string="Name")
    code = fields.Float(string="Debit")
    credit = fields.Float(string="Debit")
    debit = fields.Float(string="Debit")
    parent_id = fields.Many2one(comodel_name="hos.account", string="Parent")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
