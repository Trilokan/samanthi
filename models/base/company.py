# -*- coding: utf-8 -*-

from odoo import models, fields


class Company(models.Model):
    _name = "res.company"
    _inherit = "res.company"

    state_id = fields.Many2one(comodel_name="res.country.state", string="State", required=True)

    email = fields.Char(string="E-mail")
    contact_no = fields.Char(string="Contact No")

    # Account
    sundry_creditor_id = fields.Many2one(comodel_name="hos.account", string="Sundry Creditor")
    sundry_debtor_id = fields.Many2one(comodel_name="hos.account", string="Sundry Debtor")

    # Template
    template_appointment_order = fields.Html(string="Appointment Order Template")
    template_attendance = fields.Html(string="Monthly Attendance Report")

