from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError

class EstateInheritedUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'seller_id', domain="[('state', '!=', 'sold')]")
