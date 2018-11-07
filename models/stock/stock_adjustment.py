# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StockAdjustment(models.Model):
    _name = "stock.adjustment"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    adjusted_by = fields.Many2one(comodel_name="hos.person", string="Approve By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    adjustment_detail = fields.One2many(comodel_name="stock.adjustment.detail", inverse_name="adjustment_id", string="Adjustment Detail")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        writter = "Store Return Confirmed by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Store adjustment cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

    def generate_move(self, source_id, destination_id, recs):
        move_detail = []
        for rec in recs:
            result = {"source_id": source_id,
                      "destination_id": destination_id,
                      "reference": rec.name,
                      "product_id": rec.product_id.id,
                      "description": rec.description,
                      "quantity": rec.quantity,
                      "progress": "moved"}

            move_detail.append((0, 0, result))

        return move_detail

    def generate_picking(self, recs):
        config = self.env["product.configuration"].search([("company_id", "=", self.env.user.company_id.id)])
        source_id = config.adjustment_id.id
        destination_id = config.store_id.id

        move_detail = self.generate_move(source_id, destination_id, recs)

        if move_detail:
            picking = {"source_id": source_id,
                       "destination_id": destination_id,
                       "reference": self.name,
                       "move_detail": move_detail,
                       "progress": "moved"}

            self.env["hos.picking"].create(picking)

    @api.multi
    def trigger_approved(self):
        recs = self.env["store.adjustment.detail"].search([("adjustment_id", "=", self.id), ("quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_picking(recs)

        writter = "Stock issued by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "approved", "writter": writter})


class StockAdjustmentDetail(models.Model):
    _name = "stock.adjustment.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity", default=0)
    unit_price = fields.Float(string="Unit Price", default=0)
    comment = fields.Text(string="Comment")
    adjustment_id = fields.Many2one(comodel_name="stock.adjustment", string="Stock Adjustment")

