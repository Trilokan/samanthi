# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreReturn(models.Model):
    _name = "store.return"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, deafult=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    department_id = fields.Many2one(comodel_name="hos.department", string="Department", required=True)
    return_by = fields.Many2one(comodel_name="hos.person", string="Return By", readonly=True)
    approve_by = fields.Many2one(comodel_name="hos.person", string="Approve By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    return_detail = fields.One2many(comodel_name="store.return.detail", inverse_name="return_id", string="Return Detail")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        writter = "Store Return Confirmed by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Store Return cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

    def generate_accept(self, recs):
        accept_detail = []
        for rec in recs:
            accept_detail.append((0, 0, {"product_id": rec.product_id.id,
                                         "description": rec.description,
                                         "quantity": rec.quantity}))

        if accept_detail:
            accept = {"return_id": self.id,
                      "accept_detail": accept_detail}

            self.env["store.accept"].create(accept)

    @api.multi
    def trigger_approved(self):
        recs = self.env["store.return.detail"].search([("return_id", "=", self.id), ("quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_accept(recs)

        writter = "Store Return Approved by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "approved", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StoreReturn, self).create(vals)


class StoreReturnDetail(models.Model):
    _name = "store.return.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    description = fields.Text(string="Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    returned_quantity = fields.Float(string="Return Quantity")
    quantity = fields.Float(string="Quantity")
    return_id = fields.Many2one(comodel_name="store.return", string="Store Return")

