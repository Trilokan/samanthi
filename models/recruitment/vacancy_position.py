# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("open", "Position Open"), ("closed", "Position Closed")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class VacancyPosition(models.Model):
    _name = "vacancy.position"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position", required=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    roles = fields.Html(string="Roles & Responsibility")
    experience = fields.Html(string="Experience")
    preference = fields.Html(string="Preference")
    qualification = fields.Html(string="Qualification")
    comment = fields.Text(string="Comment")
    writter = fields.Text(string="Writter", track_visibility="always")
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    @api.multi
    def trigger_open(self):
        writter = "Vacancy position opened by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        data = {"writter": writter, "progress": "opened"}

        self.write(data)

    @api.multi
    def trigger_close(self):
        writter = "Vacancy position closed by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        data = {"writter": writter, "progress": "closed"}

        self.write(data)

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].sudo().next_by_code(self._name)
        return super(VacancyPosition, self).create(vals)
