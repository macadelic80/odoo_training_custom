from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError

class EstateInheritedUsers(models.Model):
    _name = "estate.property.users"
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'buyer_id')
