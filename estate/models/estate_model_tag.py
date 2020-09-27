from odoo import models, fields


class EstateTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_property_tag_uniqueness', 'unique(name)', 'A property tag name must be unique.'),
    ]