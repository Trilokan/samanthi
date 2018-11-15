# -*- coding: utf-8 -*-

from odoo import models, fields, api


PERSON_TYPE = [("patient", "Patient"),
               ("doctor", "Doctor"),
               ("nurse", "Nurse"),
               ("staff", "Staff"),
               ("driver", "Driver"),
               ("supplier", "Supplier"),
               ("customer", "Customer"),
               ("service", "Service")]


class HospitalPerson(models.Model):
    _name = "hos.person"
    _inherit = "hos.address"

    name = fields.Char(string="Name", required=True)
    person_uid = fields.Char(string="Person UID", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")

    person_type = fields.Selection(selection=PERSON_TYPE, string="Person Type")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    # Contact Detail (hos.address)
    contact_person = fields.Char(sring="Contact Person")
    email = fields.Char(string="Email")
    contact_no = fields.Char(string="Contact No", required=True)

    # Alternate Contact
    alternate_contact = fields.Char(string="Alternate Contact")
    alternate_email = fields.Char(string="Email")
    alternate_contact_no = fields.Char(string="Contact No", required=True)

    # Account Detail
    gst_no = fields.Char(string="GST No")
    license_no = fields.Char(string="License No")
    tin_no = fields.Char(string="TIN No")
    pan_no = fields.Char(string="PAN No")
    driving_license = fields.Char(string="Driving License")
    payable_id = fields.Many2one(comodel_name="hos.account", string="Accounts Payable")
    receivable_id = fields.Many2one(comodel_name="hos.account", string="Accounts Receivable")

    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    is_employee = fields.Boolean(string="Is Employee")

    # Smart Button

    def generate_account(self, vals):
        account = {"name": vals["name"],
                   "code": self.env['ir.sequence'].next_by_code("hos.account")}

        # Sundry Creditor
        payable_account = account
        payable_account["parent_id"] = self.env.user.company_id.sundry_creditor_id.id
        payable_id = self.env["hos.account"].create(payable_account)

        # Sundry Debtor
        receivable_account = account
        receivable_account["parent_id"] = self.env.user.company_id.sundry_debtor_id.id
        receivable_id = self.env["hos.account"].create(receivable_account)

        result = {"payable_id": payable_id.id,
                  "receivable_id": receivable_id.id}

        return result

    @api.model
    def create(self, vals):
        if "person_uid" not in vals:
            vals["person_uid"] = self.env["ir.sequence"].next_by_code(self._name)

        vals.update(self.generate_account(vals))

        return super(HospitalPerson, self).create(vals)
