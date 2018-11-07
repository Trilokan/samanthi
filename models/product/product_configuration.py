# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ProductConfiguration(models.Model):
    _name = "product.configuration"
    _inherit = "mail.thread"

    store_id = fields.Many2one(comodel_name="stock.location", string="Store Location")
    purchase_id = fields.Many2one(comodel_name="stock.location", string="Purchase Location")
    pharmacy_id = fields.Many2one(comodel_name="stock.location", string="Pharmacy Location")
    block_id = fields.Many2one(comodel_name="stock.location", string="Block List Location")
    adjustment_id = fields.Many2one(comodel_name="stock.location", string="Adjustment Location")
    assert_id = fields.Many2one(comodel_name="stock.location", string="Assert Location")
    virtual_left = fields.Integer(string="Virtual Left")
    virtual_right = fields.Integer(string="Virtual Right")
