# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class BedStatus(models.TransientModel):
    _name = "bed.status"

    date = fields.Datetime(string="Date", required=True)
    total_bed = fields.Integer(string="Total Bed", comput="_get_total_bed")
    vacant_bed = fields.Integer(string="Vacant Bed", compute="_get_vacant_bed")
    occupied_bed = fields.Integer(string="Occupied Bed", compute="_get_occupied_bed")
    vacant_ids = fields.One2many(comodel_name="bed.vacant", inverse_name="status_id")
    occupied_ids = fields.One2many(comodel_name="bed.occupied", inverse_name="status_id")

    @api.onchange('date')
    def _get_vacant_ids(self):
        bed_ids = self.env["hos.bed"].search([])
        vacant = []

        for bed_id in bed_ids:
            source_ids = self.env["patient.shifting"].search([("source_id", "=", bed_id.id)])

            if source_ids:
                source_id = source_ids.sorted(key=lambda r: r.date)[-1]
                destination_id = self.env["patient.shifting"].search([("destination_id", "=", bed_id.id),
                                                                      ("date", ">", source_id.date)])

                if not destination_id:
                    vacant.append((0, 0, {"status_id": self.id, "bed_id": bed_id.id}))

        self.vacant_ids = vacant

    @api.onchange('date')
    def _get_occupied_ids(self):
        bed_ids = self.env["hos.bed"].search([])
        occupied = []

        for bed_id in bed_ids:
            destination_ids = self.env["patient.shifting"].search([("destination_id", "=", bed_id.id)])

            if destination_ids:
                destination_id = destination_ids.sorted(key=lambda r: r.date)[-1]
                source_id = self.env["patient.shifting"].search([("source_id", "=", bed_id.id),
                                                                 ("date", ">", destination_id.date)])

                if not source_id:
                    occupied.append((0, 0, {"person_id": destination_id.person_id.id,
                                            "status_id": self.id,
                                            "bed_id": bed_id.id}))

        self.occupied_ids = occupied


class BedOccupied(models.TransientModel):
    _name = "bed.occupied"

    person_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    status_id = fields.Many2one(comodel_name="bed.status", string="Bed Status")
    bed_id = fields.Many2one(comodel_name="hos.bed", string="Bed")


class BedVacant(models.TransientModel):
    _name = "bed.vacant"

    status_id = fields.Many2one(comodel_name="bed.status", string="Bed Status")
    bed_id = fields.Many2one(comodel_name="hos.bed", string="Bed")
