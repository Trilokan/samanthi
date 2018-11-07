# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("issued", "Issued"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreIssue(models.Model):
    _name = "store.issue"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    request_id = fields.Many2one(comodel_name="store.request", string="Request", required=True)
    issue_by = fields.Many2one(comodel_name="hos.person", string="Issue By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    issue_detail = fields.One2many(comodel_name="store.issue.detail", inverse_name="issue_id", string="Issue Detail")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_cancel(self):
        writter = "Store issue cancel by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "cancel", "writter": writter})

    def generate_move(self, source_id, destination_id, recs):
        move_detail = []
        for rec in recs:
            stock = self.env["hos.stock"].get_current_stock(rec.product_id.id, source_id)

            if stock >= rec.quantity:
                result = {"source_id": source_id,
                          "destination_id": destination_id,
                          "reference": rec.name,
                          "product_id": rec.product_id.id,
                          "description": rec.description,
                          "quantity": rec.quantity,
                          "progress": "moved"}

                move_detail.append((0, 0, result))

            else:
                raise exceptions.ValidationError("Error! Product {0} has not enough stock to move".format(rec.product_id.name))

        return move_detail

    def generate_picking(self, recs):
        config = self.env["product.configuration"].search([("company_id", "=", self.env.user.company_id.id)])
        source_id = config.store_location_id.id
        destination_id = self.request_id.department_id.location_id.id

        move_detail = self.generate_move(source_id, destination_id, recs)

        if move_detail:
            picking = {"source_id": source_id,
                       "destination_id": destination_id,
                       "reference": self.name,
                       "move_detail": move_detail,
                       "progress": "moved"}

            self.env["hos.picking"].create(picking)

    def generate_remaining(self):
        issue_detail = []
        recs = self.issue_detail
        for rec in recs:
            issue_detail.append((0, 0, {"product_id": rec.product_id.id,
                                        "description": rec.description,
                                        "requested_quantity": rec.requested_quantity,
                                        "issued_quantity": rec.issued_quantity + rec.quantity}))

        if issue_detail:
            issue = {"request_id": self.request_id.id,
                     "issue_detail": issue_detail}

            self.env["store.issue"].create(issue)

    @api.multi
    def trigger_approved(self):
        recs = self.env["store.issue.detail"].search([("issue_id", "=", self.id), ("quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_picking(recs)
        self.generate_remaining()

        writter = "Stock issued by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "approved", "writter": writter})


class StoreIssueDetail(models.Model):
    _name = "store.issue.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Item", required=True)
    description = fields.Text(string="Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    requested_quantity = fields.Float(string="Requested Quantity")
    issued_quantity = fields.Float(string="Issued Quantity")
    quantity = fields.Float(string="Issuing Quantity")
    issue_id = fields.Many2one(comodel_name="store.issue", string="Store Issue")

