# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Reconciliation(models.Model):
    _name = "hos.reconcile"

    name = fields.Char(string="Name")

    partial_ids = fields.One2many(comodel_name="journal.items",
                                  inverse_name="reconcile_id",
                                  string="Partial Reconciliation")

    full_ids = fields.One2many(comodel_name="journal.items",
                               inverse_name="reconcile_part_id",
                               string="Full Reconciliation")
