# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class HosMove(models.Model):
    _name = "hos.move"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    source_id = fields.Many2one(comodel_name="stock.location", string="Source Location", required=True)
    destination_id = fields.Many2one(comodel_name="stock.location", string="Destination Location", required=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Item", required=True)
    description = fields.Text(string="Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity", default=0, required=True)
    unit_price = fields.Float(string="Unit Price", default=0, required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    reference = fields.Text(string="Reference")

    @api.constrains("source_id", "product_id")
    def check_current_stock(self):
        # Virtual Source
        conf = self.env["product.configuration"].search([("company_id", "=", self.env.user.company_id.id)])

        if (self.source_id.location_left >= conf.virtual_left) and (self.source_id.location_right <= conf.virtual_right):
            return True

        current_stock = self.env["hos.stock"].get_current_stock(self.product_id.id, self.source_id.id)

        if self.quantity > (current_stock - self.quantity):
            raise exceptions.ValidationError("Error! Please check stock")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(HosMove, self).create(vals)
