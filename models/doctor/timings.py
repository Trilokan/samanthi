# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime


# Doctor Timings
class DutyTimings(models.Model):
    _name = "duty.timings"
    _inherit = "mail.thread"
    _rec_name = "person_id"

    person_id = fields.Many2one(comodel_name="hos.person", string="Employee", required=True)

    monday_fn_from_time = fields.Float(string="Monday FN From Time")
    monday_fn_till_time = fields.Float(string="Monday FN Till Time")
    monday_an_from_time = fields.Float(string="Monday AN From Time")
    monday_an_till_time = fields.Float(string="Monday AN Till Time")

    tuesday_fn_from_time = fields.Float(string="Tuesday FN From Time")
    tuesday_fn_till_time = fields.Float(string="Tuesday FN Till Time")
    tuesday_an_from_time = fields.Float(string="Tuesday AN From Time")
    tuesday_an_till_time = fields.Float(string="Tuesday AN Till Time")

    wednesday_fn_from_time = fields.Float(string="Wednesday FN From Time")
    wednesday_fn_till_time = fields.Float(string="Wednesday FN Till Time")
    wednesday_an_from_time = fields.Float(string="Wednesday AN From Time")
    wednesday_an_till_time = fields.Float(string="Wednesday AN Till Time")

    thursday_fn_from_time = fields.Float(string="Thursday FN From Time")
    thursday_fn_till_time = fields.Float(string="Thursday FN Till Time")
    thursday_an_from_time = fields.Float(string="Thursday AN From Time")
    thursday_an_till_time = fields.Float(string="Thursday AN Till Time")

    friday_fn_from_time = fields.Float(string="Friday FN From Time")
    friday_fn_till_time = fields.Float(string="Friday FN Till Time")
    friday_an_from_time = fields.Float(string="Friday AN From Time")
    friday_an_till_time = fields.Float(string="Friday AN Till Time")

    saturday_fn_from_time = fields.Float(string="Saturday FN From Time")
    saturday_fn_till_time = fields.Float(string="Saturday FN Till Time")
    saturday_an_from_time = fields.Float(string="Saturday AN From Time")
    saturday_an_till_time = fields.Float(string="Saturday AN Till Time")

    sunday_fn_from_time = fields.Float(string="Sunday FN From Time")
    sunday_fn_till_time = fields.Float(string="Sunday FN Till Time")
    sunday_an_from_time = fields.Float(string="Sunday AN From Time")
    sunday_an_till_time = fields.Float(string="Sunday AN Till Time")

