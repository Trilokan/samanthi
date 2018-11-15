# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime


# Doctor Timings
class DutyTimings(models.Model):
    _name = "duty.timings"
    _inherit = "mail.thread"
    _rec_name = "person_id"

    person_id = fields.Many2one(comodel_name="hos.person", string="Employee", required=True)
    timing_detail = fields.One2many(comodel_name="timings.detail", inverse_name="timings_id", string="Timings")

    @api.model
    def create(self, vals):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        day_list = []
        for day in days:
            day_list.append((0, 0, {"name": day}))

        vals["timing_detail"] = day_list

        return super(DutyTimings, self).create(vals)


class TimingsDetail(models.Model):
    _name = "timings.detail"

    name = fields.Char(string="Days", readonly=True)
    fn_from_time = fields.Integer(string="FN From Time")
    fn_till_time = fields.Integer(string="FN Till Time")

    an_from_time = fields.Integer(string="AN From Time")
    an_till_time = fields.Integer(string="AN Till Time")
    timings_id = fields.Many2one(comodel_name="duty.timings", string="Duty Timings")
