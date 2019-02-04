# -*- coding: utf-8 -*-

from odoo import models, fields


class StockLocation(models.Model):
    _name = "stock.location"

    name = fields.Char(string="Name", required=True)
    location_uid = fields.Char(string="Code", compute="_get_code")
    location_left = fields.Integer(string="Location Left", required=True)
    location_right = fields.Integer(string="Location Right", required=True)

    _sql_constraints = [("location_uid", "unique(location_uid)", "Stock Location must be unique")]

    def _get_code(self):
        for record in self:
            recs = self.env["stock.location"].search([("location_left", "<=", record.location_left),
                                                      ("location_right", ">=", record.location_right)])

            recs = recs.sorted(key=lambda r: r.location_left)
            record.code = "/".join(str(x.name) for x in recs)
