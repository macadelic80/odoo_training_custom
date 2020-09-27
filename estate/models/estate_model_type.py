from odoo import models, fields


class EstateTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many('estate.property', 'property_type_id')
    _sql_constraints = [
        ('check_property_type_uniqueness', 'unique(name)', 'A property type name must be unique.'),
    ]