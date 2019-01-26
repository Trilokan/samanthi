# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
PROGRESS = [("draft", "Draft"), ("registered", "Registered")]


class RegisterPayment(models.Model):
    _name = "register.payment"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="qin.person", string="Person", required=True)
    journal_type_id = fields.Many2one(comodel_name="journal.type", string="Journal Type", required=True)
    invoice_id = fields.Many2one(comodel_name="qin.invoice", string="Invoice", required=True)
    amount = fields.Float(string="Amount")
    progress = fields.Selection(selection=PROGRESS, string="Progress", default="draft")

    # journal_ids = fields.One2many(comodel_name="journal.item", inverse_name="j")
