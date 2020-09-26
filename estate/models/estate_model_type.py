from odoo import models, fields


class EstateTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(required=True)
