# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Account(models.Model):
    _name = "hos.account"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    balance = fields.Float(string="Balance")
    parent_id = fields.Many2one(comodel_name="hos.account", string="Parent")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
