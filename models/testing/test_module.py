# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TestModule(models.Model):
    _name = "test.module"

    name = fields.Char(string="Name")
    detail_ids = fields.One2many(comodel_name="test.module.detail", inverse_name="test_id")


class DetailItems(models.Model):
    _name = "test.module.detail"

    name = fields.Char(string="Name")
    value = fields.Integer(string="Value")
    test_id = fields.Many2one(comodel_name="test.module", string="Test Module")


