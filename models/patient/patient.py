# -*- coding: utf-8 -*-

from odoo import models, fields, api

BLOOD_GROUP = [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'),
               ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'), ('o-', 'O-')]
GENDER = [('male', 'Male'), ('female', 'Female')]
MARITAL_STATUS = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]


class Patient(models.Model):
    _name = "qin.patient"

    name = fields.Char(string="Name", required=True)
    patient_uid = fields.Char(string="Employee ID", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Small Image")
    person_id = fields.Many2one(comodel_name="qin.person", string="Person")

    # Contact Details
    email = fields.Char(string="e-Mail")
    mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Phone")

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

    # Personnel Details
    age = fields.Integer(string="Age")
    blood_group = fields.Selection(selection=BLOOD_GROUP, string="Blood Group")
    marital_status = fields.Selection(selection=MARITAL_STATUS, string="Marital Status")
    gender = fields.Selection(selection=GENDER, string="Gender")
    caste = fields.Char(string="Caste")
    religion_id = fields.Many2one(comodel_name="qin.religion", string="Religion")
    physically_challenged = fields.Boolean(string="Physically Challenged")
    nationality_id = fields.Many2one(comodel_name="res.country")
    mother_tongue_id = fields.Many2one(comodel_name="qin.language", string="Mother Tongue")
    language_known_ids = fields.Many2many(comodel_name="qin.language", string="Language Known")
    personnel_mobile = fields.Char(string="Personnel Mobile")
    personnel_email = fields.Char(string="Personnel Email")
    permanent_address = fields.Text(string="Permanent Address")
    family_member_ids = fields.One2many(comodel_name="qin.address", inverse_name="employee_id")

    # Medical Detail
    allergic_towards = fields.Text(string="Allergic Towards")

    # Attachment
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
