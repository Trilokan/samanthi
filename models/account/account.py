# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QinAccount(models.Model):
    _name = "qin.account"

    name = fields.Char(string="Name", required=True)
    account_uid = fields.Char(string="Code", readonly=True)
    is_reconcile = fields.Boolean(string="Allow Reconcile")
    credit = fields.Float(string="Credit", compute="_get_credit")
    debit = fields.Float(string="Debit", compute="_get_debit")

    def _get_credit(self):
        for rec in self:
            rec.credit = 0

        return True

    def _get_debit(self):
        for rec in self:
            rec.debit = 0

        return True

    @api.model
    def create(self, vals):
        vals["account_uid"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(QinAccount, self).create(vals)
