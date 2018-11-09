# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class AssertsCapitalisation(models.Model):
    _name = "asserts.capitalisation"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    adjusted_by = fields.Many2one(comodel_name="hos.person", string="Approve By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    capitalise_detail = fields.One2many(comodel_name="asserts.capitalisation.detail", inverse_name="capitalise_id")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        writter = "Asserts capitalisation confirmed by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Asserts capitalisation cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

    def generate_move(self, recs):
        config = self.env["product.configuration"].search([("company_id", "=", self.env.user.company_id.id)])

        if self.adjust_type == "increase":
            source_id = config.adjustment_id.id
            destination_id = config.store_id.id

        elif self.adjust_type == "decrease":
            source_id = config.store_id.id
            destination_id = config.adjustment_id.id

        for rec in recs:
            result = {"source_id": source_id,
                      "destination_id": destination_id,
                      "reference": rec.name,
                      "product_id": rec.product_id.id,
                      "description": rec.description,
                      "quantity": rec.quantity,
                      "unit_price": rec.unit_price,
                      "progress": "moved"}

            self.env["hos.move"].create(result)

    @api.multi
    def trigger_approve(self):
        adjusted_by = self.env.user.person_id.id
        recs = self.env["stock.adjustment.detail"].search([("adjustment_id", "=", self.id), ("quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_move(recs)

        writter = "Stock issued by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "approved", "writter": writter, "adjusted_by": adjusted_by})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(AssertsCapitalisation, self).create(vals)


class AssertsCapitalisationDetail(models.Model):
    _name = "asserts.capitalisation.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Item", required=True)
    description = fields.Text(string="Item Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity", default=0, required=True)
    comment = fields.Text(string="Comment")
    capitalise_id = fields.Many2one(comodel_name="asserts.capitalisation", string="Capitalisation")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="capitalise_id.progress")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(AssertsCapitalisationDetail, self).create(vals)
