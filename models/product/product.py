# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class Product(models.Model):
    _name = "hos.product"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", readonly=True)
    product_group_id = fields.Many2one(comodel_name="product.group", string="Group", required=True)
    sub_group_id = fields.Many2one(comodel_name="product.sub.group", string="Sub Group", required=True)
    category_id = fields.Many2one(comodel_name="product.category", string="Category", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", required=True)
    hsn_code = fields.Char(string="HSN Code", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    description = fields.Text(string="Description")
    payable = fields.Many2one(comodel_name="hos.account", string="Accounts Payable")
    receivable = fields.Many2one(comodel_name="hos.account", string="Accounts Receivable")
    warehouse_ids = fields.One2many(comodel_name="stock.warehouse",
                                    string="Warehouse",
                                    compute="_get_warehouse_ids")

    _sql_constraints = [("code", "unique(code)", "Product Code must be unique")]

    @api.one
    def _get_warehouse_ids(self):
        config = self.env["product.configuration"].search([("company_id", "=", self.env.user.company_id.id)])
        domain = [('location_id.location_left', '>=', config.virtual_left),
                  ('location_id.location_right', '<=', config.virtual_right)]

        self.warehouse_ids = self.env["stock.warehouse"].search(domain)

    @api.multi
    def trigger_confirm(self):
        config = self.env["product.configuration"].search([("company_id", "=", self.env.user.company_id.id)])
        store_location_id = config.store_id.id

        if not store_location_id:
            raise exceptions.ValidationError("Default Product Location is not set")

        # Generate Warehouse of default store location
        self.env["stock.warehouse"].create({"product_id": self.id, "location_id": store_location_id})

        # Generate Code on confirmation
        code = "{0}/{1}/{2}".format(self.product_group_id.code,
                                    self.sub_group_id.code,
                                    self.env["ir.sequence"].next_by_code(self._name))

        self.write({"progress": "confirmed", "code": code})

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.code, record.name)
            result.append((record.id, name))
        return result
