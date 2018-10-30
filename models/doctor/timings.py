# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime


# Hospital Timings
class HospitalTimings(models.Model):
    _name = "hos.timings"
    _inherit = "mail.thread"
    _rec_name = "employee_id"

    employee_id = fields.Many2one(comodel_name="hos.person", string="Employee", required=True)
    timing_detail = fields.One2many(comodel_name="timings.detail", inverse_name="timings_id", string="Timings")


class TimingsDetail(models.Model):
    _name = "timings.detail"

    name = fields.Char(string="Days")
    fn_from_time = fields.Integer(string="FN From Time")
    fn_till_time = fields.Integer(string="FN Till Time")

    an_from_time = fields.Integer(string="AN From Time")
    an_till_time = fields.Integer(string="AN Till Time")
