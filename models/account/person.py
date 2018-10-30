# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Person(models.Model):
    _name = "hos.person"

    name = fields.Char(string="Name")
    payable_id = fields.Many2one(comodel_name="hos.account", string="Payable")
    receivable_id = fields.Many2one(comodel_name="hos.account", string="Receivable")
