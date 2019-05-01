# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo import http
import json


class ReportController(http.Controller):

    @http.route('/suggestions', type='http', auth='user', methods=['GET'])
    def suggestions(self, jsdata):
        option = {
            "title": {
                "text": 'ECharts entry example'
            },
            "tooltip": {},
            "legend": {
                "data": ['Sales']
            },
            "xAxis": {
                "data": ["shirt", "cardign", "chiffon shirt", "pants", "heels", "socks"]
            },
            "yAxis": {},
            "series": [{
                "name": 'Sales',
                "type": 'bar',
                "data": [5, 20, 36, 10, 10, 20]
            }]
        }

        print json.dumps(option)

        return json.dumps(option)


# Report Tool
class ReportTool(models.Model):
    _name = "report.tool"

    name = fields.Char(string="Category")
    employee_ids = fields.Many2many(comodel_name="hr.employee")

