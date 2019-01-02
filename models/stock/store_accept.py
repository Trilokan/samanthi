# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("accepted", "Accepted"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreAccept(models.Model):
    _name = "store.accept"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    return_id = fields.Many2one(comodel_name="store.return", string="Return", required=True)
    accept_by = fields.Many2one(comodel_name="lam.person", string="Accept By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    accept_detail = fields.One2many(comodel_name="store.accept.detail", inverse_name="accept_id", string="Accept Detail")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_cancel(self):
        writter = "Store accept cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

    def generate_move(self, recs):
        config = self.env["product.configuration"].search([("company_id", "=", self.env.user.company_id.id)])

        source_id = self.department_id.location_id.id
        destination_id = config.store_id.id

        for rec in recs:
            result = {"source_id": source_id,
                      "destination_id": destination_id,
                      "reference": rec.name,
                      "product_id": rec.product_id.id,
                      "description": rec.description,
                      "quantity": rec.quantity,
                      "progress": "moved"}

            self.env["hos.move"].create(result)

    def generate_remaining(self):
        accept_detail = []
        recs = self.accept_detail
        for rec in recs:
            accepted_quantity = rec.accepted_quantity + rec.quantity
            if rec.returned_quantity > accepted_quantity:
                accept_detail.append((0, 0, {"product_id": rec.product_id.id,
                                             "description": rec.description,
                                             "returned_quantity": rec.returned_quantity,
                                             "accepted_quantity": accepted_quantity}))

        if accept_detail:
            accept = {"return_id": self.return_id.id,
                      "department_id": self.department_id.id,
                      "accept_detail": accept_detail}

            self.env["store.accept"].create(accept)

    @api.multi
    def trigger_accept(self):
        accept_by = self.env.user.person_id.id
        recs = self.env["store.accept.detail"].search([("accept_id", "=", self.id), ("quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_move(recs)
        self.generate_remaining()

        writter = "Stock accepted by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "accepted", "writter": writter, "accept_by": accept_by})


class StoreAcceptDetail(models.Model):
    _name = "store.accept.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    description = fields.Text(string="Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    returned_quantity = fields.Float(string="Return Quantity", default=0, required=True)
    accepted_quantity = fields.Float(string="Issued Quantity", default=0, required=True)
    quantity = fields.Float(string="Accepting Quantity", default=0, required=True)
    accept_id = fields.Many2one(comodel_name="store.accept", string="Store Accept")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="accept_id.progress")

    @api.constrains("quantity")
    def check_issue_quantity(self):
        if self.quantity > (self.returned_quantity - self.accepted_quantity):
            raise exceptions.ValidationError("Error! Issue quantity more than requested")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StoreAcceptDetail, self).create(vals)
