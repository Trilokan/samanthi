# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class Product(models.Model):
    _name = "hos.product"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    product_group_id = fields.Many2one(comodel_name="product.group", string="Group")
    product_sub_group_id = fields.Many2one(comodel_name="product.sub.group", string="Sub Group")
    category_id = fields.Many2one(comodel_name="product.category", string="Category")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM")
    hsn_code = fields.Char(string="HSN Code")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    warehouse_ids = fields.One2many(comodel_name="stock.warehouse",
                                    inverse_name="product_id",
                                    string="Warehouse",
                                    domain=lambda self: self._get_warehouse_ids(),
                                    readonly=True)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    def _get_warehouse_ids(self):
        config = self.env["product.configuration"].search([("company_id", "=", self.env.user.company_id.id)])
        domain = [('location_id.location_left', '>=', config.virtual_location_left),
                  ('location_id.location_right', '<=', config.virtual_location_right)]

        virtual_location = self.env["stock.warehouse"].search(domain)

        return [("id", "not in", virtual_location.ids)]

    @api.multi
    def trigger_confirm(self):
        config = self.env["product.configuration"].search([("company_id", "=", self.env.user.company_id.id)])
        store_location_id = config.store_location_id.id

        if not store_location_id.id:
            raise exceptions.ValidationError("Default Product Location is not set")

        self.env["stock.warehouse"].create({"product_id": self.id, "location_id": store_location_id})
        self.write({"progress": "confirmed"})

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.code, record.name)
            result.append((record.id, name))
        return result

    @api.model
    def create(self, vals):
        group_id = self.env["product.group"].search([("id", "=", vals["group_id"])])
        sub_group_id = self.env["product.sub.group"].search([("id", "=", vals["sub_group_id"])])
        code = "{0}/{1}/{2}".format(group_id.code,
                                    sub_group_id.code,
                                    self.env["ir.sequence"].next_by_code(self._name))

        vals["code"] = code

        return super(Product, self).create(vals)
