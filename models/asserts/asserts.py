# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Assert
class Assert(models.Model):
    _name = "qin.asserts"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)

    # Manufacturing Details
    product_id = fields.Many2one(comodel_name="qin.product", string="Product", required=True)
    manufacturer = fields.Char(string="Manufacturer")
    manufactured_date = fields.Date(string="Date of Manufactured")
    expiry_date = fields.Date(string="Date of Expiry")
    serial_no = fields.Char(string="Serial No")
    model_no = fields.Char(string="Manufacturer")
    warranty_date = fields.Date(string="Warranty Date")

    # Seller Details
    vendor_id = fields.Many2one(comodel_name="qin.person", string="Vendor")
    order_date = fields.Date(string="Order Date")
    order_id = fields.Many2one(comodel_name="purchase.order", string="Purchase Order")
    purchase_date = fields.Date(string="Date of Purchase")
    invoice_id = fields.Many2one(comodel_name="purchase.invoice", string="Purchase Invoice")
    # vendor_contact = ""
    # vendor_address = ""

    # Maintenance Details
    maintenance_id = fields.Many2one(comodel_name="qin.person", string="Maintenance")
    # service_contact = ""
    # service_address = ""
    maintenance_details = fields.One2many(comodel_name="asserts.maintenance",
                                          inverse_name="asserts_id",
                                          string="Maintenance Details")
    notification_details = fields.One2many(comodel_name="asserts.reminder",
                                           inverse_name="asserts_id",
                                           string="Notification Details")

    # Accounting Details
    account_id = fields.Many2one(comodel_name="qin.account", string="Account")
    depreciation_percentage = fields.Float(string="Depreciation Percentage")
    responsible_id = fields.Many2one(comodel_name="qin.person", string="Responsible Person")
    is_working = fields.Boolean(string="Is Working")
    is_condem = fields.Boolean(string="Is Condemed")
    attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id, readonly=True)

    _sql_constraints = [('unique_name', 'unique (name)', 'Error! Assert must be unique')]

    @api.multi
    def trigger_confirm(self):
        writter = "Asserts capitalisation confirmed by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "confirmed", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        vals["writter"] = "Assert Created by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        return super(Assert, self).create(vals)


class AssertMaintenance(models.Model):
    _name = "asserts.maintenance"
    _inherit = "mail.thread"
    _rec_name = "asserts_id"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    asserts_id = fields.Many2one(comodel_name="qin.asserts", string="Assert")
    person_id = fields.Many2one(comodel_name="qin.person", string="Maintenance", required=True)
    description = fields.Text(string="Description", required=True)
    attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.model
    def create(self, vals):
        vals["writter"] = "Assert Maintenance Created by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        return super(AssertMaintenance, self).create(vals)


class AssertNotification(models.Model):
    _name = "asserts.reminder"
    _inherit = "mail.thread"
    _rec_name = "asserts_id"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    asserts_id = fields.Many2one(comodel_name="qin.asserts", string="Assert")
    person_id = fields.Many2one(comodel_name="qin.person", string="Notify", required=True)
    description = fields.Text(string="Description", required=True)

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.model
    def create(self, vals):
        vals["writter"] = "Assert reminder Created by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        return super(AssertNotification, self).create(vals)
