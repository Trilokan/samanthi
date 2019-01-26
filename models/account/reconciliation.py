# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QinReconciliation(models.Model):
    _name = "qin.reconciliation"

    name = fields.Char(string="Name", readonly=True)
    reconcile_ids = fields.One2many(comodel_name="journal.item", inverse_name="reconcile_id")
    part_reconcile_ids = fields.One2many(comodel_name="journal.item", inverse_name="part_reconcile_id")
