# -*- coding: utf-8 -*-

from odoo import models, fields


class LeaveLevel(models.Model):
    _name = "leave.level"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    level_detail = fields.One2many(comodel_name="leave.level.detail", inverse_name="level_id", string="Level Detail")

    _sql_constraints = [("code", "unique(code)", "Leave Level must be unique")]


class LeaveLevelDetail(models.Model):
    _name = "leave.level.detail"

    type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type", required=True)
    sequence = fields.Integer(string="Sequence", default=0, required=True)
    credit = fields.Float(string="Credit", default=0, required=True)
    level_id = fields.Many2one(comodel_name="leave.level", string="Level")

    _sql_constraints = [("type_level", "unique(type_id, level_id)", "Leave Type must be unique")]
