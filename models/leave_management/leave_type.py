# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LeaveType(models.Model):
    _name = "leave.type"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    account_id = fields.Many2one(comodel_name="leave.account", string="Leave Account", readonly=True)

    _sql_constraints = [("code", "unique(code)", "Leave Type must be unique")]

    @api.model
    def create(self, vals):
        leave_account_id = self.env["leave.account"].create({"name": vals["name"]})
        vals["account_id"] = leave_account_id.id
        return super(LeaveType, self).create(vals)
