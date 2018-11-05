# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Reconciliation(models.Model):
    _name = "hos.reconcile"

    name = fields.Char(string="Name")

    partial_reconcile_ids = fields.One2many(comodel_name="journal.items",
                                            inverse_name="reconcile_part_id",
                                            string="Partial Reconciliation")

    reconcile_ids = fields.One2many(comodel_name="journal.items",
                                    inverse_name="reconcile_id",
                                    string="Full Reconciliation")

    def swap_reconciliation_id(self, rec):
        rec.reconcile_id = rec.reconcile_part_id.id
        rec.reconcile_part_id = False

    def check_reconciliation(self, rec_id):
        partial_ids = self.env["journal.items"].search([("reconcile_part_id", "=", rec_id)])

        credit = sum(partial_ids.mapped('credit'))
        debit = sum(partial_ids.mapped('debit'))

        if credit == debit:
            map(self.swap_reconciliation_id, partial_ids)

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(Reconciliation, self).create(vals)
