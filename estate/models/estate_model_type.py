from odoo import models, fields, api, _


class EstateTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')

    offer_count = fields.Integer(compute="_compute_offer_count")
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for r in self:
            r.offer_count = len(r.offer_ids)

    def action_open_offers(self):
        self.ensure_one()
        offer_ids = self.offer_ids
        domain = [('id', 'in', offer_ids)]
        action = {
            'name': _('Offers'),
            'view_type': 'tree',
            'view_mode': 'list,form',
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',
            'context': self.env.context,
            'domain': domain,
        }
        return action

    _sql_constraints = [
        ('check_property_type_uniqueness', 'unique(name)', 'A property type name must be unique.'),
    ]
