# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QinPerson(models.Model):
    _name = "qin.person"

    name = fields.Char(string="Name", required=True)
    person_uid = fields.Char(string="ID Card No", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Small Image")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    # Professional Details
    email = fields.Char(string="e-Mail")
    mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Phone")
    contact_name = fields.Char(string="Contact Name")
    contact_position = fields.Char(string="Position")

    # Address in Detail
    door_no = fields.Char(string="Door No")
    building_name = fields.Char(string="Building Name")
    street_1 = fields.Char(string="Street 1")
    street_2 = fields.Char(string="Street 2")
    locality = fields.Char(string="locality")
    landmark = fields.Char(string="landmark")
    city = fields.Char(string="City")
    state_id = fields.Many2one(comodel_name="res.country.state", string="State",
                               default=lambda self: self.env.user.company_id.state_id.id)
    country_id = fields.Many2one(comodel_name="res.country", string="Country")
    pin_code = fields.Char(string="Pincode")

    # Account Details
    gst_no = fields.Char(string="GST No")
    license_no = fields.Char(string="License No")
    tin_no = fields.Char(string="TIN No")
    pan_no = fields.Char(string="PAN No")
    driving_license = fields.Char(string="Driving License")
    payable_id = fields.Many2one(comodel_name="qin.account", string="Accounts Payable")
    receivable_id = fields.Many2one(comodel_name="qin.account", string="Accounts Receivable")

    @api.model
    def create(self, vals):
        if "person_uid" not in vals:
            vals["person_uid"] = self.env["ir.sequence"].next_by_code(self._name)

        return super(QinPerson, self).create(vals)
