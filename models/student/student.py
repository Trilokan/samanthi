# -*- coding: utf-8 -*-

from odoo import models, fields, api

BLOOD_GROUP = [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'),
               ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'), ('o-', 'O-')]
GENDER = [('male', 'Male'), ('female', 'Female')]


class SchoolStudent(models.Model):
    _name = "sch.student"
    _inherit = ["lam.address"]
    _description = "School student masters"

    name = fields.Char(string="Name", required=True)
    student_uid = fields.Char(string="Student ID", readonly=True)
    image = fields.Binary(string="Image")
    user_id = fields.Many2one(comodel_name="res.users", string="User")
    person_id = fields.Many2one(comodel_name="lam.person", string="Partner")

    # Personal Details
    age = fields.Integer(string="Age")
    blood_group = fields.Selection(selection=BLOOD_GROUP, string="Blood Group")
    gender = fields.Selection(selection=GENDER, string="Gender")
    caste = fields.Char(string="Caste")
    religion_id = fields.Many2one(comodel_name="lam.religion", string="Religion")
    physically_challenged = fields.Boolean(string="Physically Challenged")
    nationality_id = fields.Many2one(comodel_name="res.country")
    mother_tongue_id = fields.Many2one(comodel_name="lam.language", string="Mother Tongue")
    language_known_ids = fields.Many2many(comodel_name="lam.language", string="Language Known")
    personnel_mobile = fields.Char(string="Personnel Mobile")
    personnel_email = fields.Char(string="Personnel Email")
    permanent_address = fields.Text(string="Permanent Address")
    family_member_ids = fields.One2many(comodel_name="lam.contact",
                                        inverse_name="employee_id",
                                        string="Family Members")

    # Contact
    email = fields.Char(string="Email")
    contact_no = fields.Char(string="Contact No", required=True)
    alternate_contact_no = fields.Char(string="Alternate Contact", required=True)

    # Account Details
    bank = fields.Char(string="Bank")
    account_no = fields.Char(string="Account No")
    aadhaar_card = fields.Char(string="Aadhaar Card")

    # Academic Details
    section_id = fields.Many2one(comodel_name="sch.section", string="Section")
    supervisor_id = fields.Many2one(comodel_name="lam.person", string="Class Teacher")
    # past_section_ids = fields.Many2many(comodel_name="academic.section", string="History")

    # Other Details



