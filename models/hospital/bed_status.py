# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class BedStatus(models.TransientModel):
    _name = "bed.status"

    date = fields.Datetime(string="Date", required=True)
