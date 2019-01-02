# -*- coding: utf-8 -*-

from odoo import models, fields, api

BLOOD_GROUP = [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'),
               ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'), ('o-', 'O-')]
GENDER = [('male', 'Male'), ('female', 'Female')]
MARITAL_STATUS = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]


class Employee(models.Model):
    _name = "hr.employee"
    _inherit = ["lam.address"]

    name = fields.Char(string="Name", required=True)
    employee_uid = fields.Char(string="Employee ID", readonly=True)
    image = fields.Binary(string="Image")
    user_id = fields.Many2one(comodel_name="res.users", string="User")
    person_id = fields.Many2one(comodel_name="lam.person", string="Partner")

    # Contact
    email = fields.Char(string="Email")
    contact_no = fields.Char(string="Contact No", required=True)
    alternate_contact_no = fields.Char(string="Alternate Contact", required=True)

    # Account Details
    bank = fields.Char(string="Bank")
    account_no = fields.Char(string="Account No")
    aadhaar_card = fields.Char(string="Aadhaar Card")
    pan_card = fields.Char(string="Pan Card")
    driving_license = fields.Char(string="Driving License")
    passport = fields.Char(string="Passport")
    epf_no = fields.Char(string="EPF No")
    epf_nominee = fields.Char(string="EPF Nominee")

    # HR Details
    doj = fields.Date(string="Date of Joining", required=False)
    date_of_relieving = fields.Date(string="Date of Relieving")
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    designation_id = fields.Many2one(comodel_name="hr.designation", string="Designation")
    reporting_to_id = fields.Many2one(comodel_name="hr.employee", string="Reporting To")
    employee_category_id = fields.Many2one(comodel_name="hr.category", string="Employee Category", required=True)
    qualification_ids = fields.One2many(comodel_name="hr.qualification",
                                        inverse_name="employee_id",
                                        string="Qualification")
    experience_ids = fields.One2many(comodel_name="hr.experience",
                                     inverse_name="employee_id",
                                     string="Experience")

    # Personnel Details
    age = fields.Integer(string="Age")
    blood_group = fields.Selection(selection=BLOOD_GROUP, string="Blood Group")
    marital_status = fields.Selection(selection=MARITAL_STATUS, string="Marital Status")
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

    # Leave
    leave_level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level")
    leave_account_id = fields.Many2one(comodel_name="leave.account", string="Leave Account")

    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    def generate_leave_account(self, vals):
        leave_account_id = self.env["leave.account"].create({"name": vals["name"]})
        return leave_account_id.id

    def generate_person(self, vals):
        employee_category_id = self.env["hr.category"].search([("id", "=", vals["employee_category_id"])])
        category_type_id = self.env["person.type"].search([("name", "=", employee_category_id.name)])
        employee_type_id = self.env["person.type"].search([("name", "=", "Staff")])

        data = {"name": vals["name"],
                "contact_no": vals["contact_no"],
                "email": vals.get("email", False),
                "alternate_contact_no": vals.get("alternate_contact_no", False),
                "person_uid": vals["employee_uid"],
                "type_ids": [(6, 0, [category_type_id.id, employee_type_id.id])],
                "person_type": employee_category_id.name.lower()}

        person_id = self.env["lam.person"].create(data)

        return person_id.id

    @api.model
    def create(self, vals):
        vals["employee_uid"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["leave_account_id"] = self.generate_leave_account(vals)
        vals["person_id"] = self.generate_person(vals)

        return super(Employee, self).create(vals)
