# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime

ADMISSION_INFO = [("draft", "Draft"), ("admitted", "Admitted")]
DISCHARGE_INFO = [("draft", "Draft"),
                  ("doctor_approve", "Doctor Approve"),
                  ("account_approve", "Account Approve"),
                  ("discharged", "Discharged")]
ADMIT_DISC_TYPE = [("normal", "Normal"), ("emergency", "Emergency")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class AdmissionDischarge(models.Model):
    _name = "admission.discharge"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    writter = fields.Char(string="Writter", track_visibility="always")

    # Contact
    patient_id = fields.Many2one(comodel_name="lam.person", string="Patient", required=True)
    person_uid = fields.Char(string="Patient ID", related="patient_id.person_uid")
    image = fields.Binary(string="Image", related="patient_id.image")
    email = fields.Char(string="Email", related="patient_id.email")
    contact_no = fields.Char(string="Mobile", related="patient_id.contact_no")

    # Address
    door_no = fields.Char(string="Door No", related="patient_id.door_no")
    building_name = fields.Char(string="Building Name", related="patient_id.building_name")
    street_1 = fields.Char(string="Street 1", related="patient_id.street_1")
    street_2 = fields.Char(string="Street 2", related="patient_id.street_2")
    locality = fields.Char(string="locality", related="patient_id.locality")
    landmark = fields.Char(string="landmark", related="patient_id.landmark")
    city = fields.Char(string="City", related="patient_id.city")
    state_id = fields.Many2one(comodel_name="res.country.state", string="State", related="patient_id.state_id")
    country_id = fields.Many2one(comodel_name="res.country", string="Country", related="patient_id.country_id")
    pin_code = fields.Char(string="Pincode", related="patient_id.pin_code")

    # Admission Details
    admission_on = fields.Date(string="Admission Date", default=CURRENT_DATE)
    admission_by = fields.Many2one(comodel_name="lam.person", string="Admit By")
    admission_reason = fields.Many2one(comodel_name="admission.reason", string="Reason")
    admission_status = fields.Selection(selection=ADMIT_DISC_TYPE, string="Patient Status")
    admission_progress = fields.Selection(selection=ADMISSION_INFO, string="Admission Progress", default="draft")
    admission_comment = fields.Text(string="Comment")
    admission_attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    admission_bed_id = fields.Many2one(comodel_name="hos.bed", string="Bed")

    # Discharge Details
    discharge_on = fields.Date(string="Discharge Date")
    discharge_by = fields.Many2one(comodel_name="lam.person", string="Discharge By")
    discharge_reason = fields.Many2one(comodel_name="admission.reason", string="Reason")
    discharge_status = fields.Selection(selection=ADMIT_DISC_TYPE, string="Patient Status")
    discharge_progress = fields.Selection(selection=DISCHARGE_INFO, string="Discharge Progress", default="draft")
    discharge_comment = fields.Text(string="Comment")
    discharge_attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    discharge_bed_id = fields.Many2one(comodel_name="hos.bed", string="Bed")

    treatment_id = fields.Many2one(comodel_name="hos.treatment", string="Treatment")

    @api.multi
    def trigger_admit(self):
        writter = "Admitted by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "admitted", "writter": writter})

    @api.multi
    def trigger_discharge(self):
        writter = "Discharged by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "admitted", "writter": writter})

    @api.multi
    def trigger_doctor_approve(self):
        self.check_payment()
        writter = "Dr {0} approved on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "admitted", "writter": writter})

    @api.multi
    def trigger_account_approve(self):
        self.check_payment()
        writter = "Account {0} approved on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "admitted", "writter": writter})

    def check_payment(self):
        pass







