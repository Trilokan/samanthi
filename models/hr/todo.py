# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("done", "Done")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class HospitalTodo(models.TransientModel):
    _name = "hos.todo"

    person_id = fields.Many2one(comodel_name="lam.person", string="Employee")
    date = fields.Date(string="Date", default=CURRENT_DATE)
    description = fields.Text(string="Description")
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft")

    @api.multi
    def trigger_done(self):
        self.write({"progress": "done"})
