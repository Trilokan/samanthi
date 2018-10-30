# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Account(models.Model):
    _name = "hos.account"

    name = fields.Char(string="Name")
    