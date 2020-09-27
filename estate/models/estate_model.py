from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare

class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        help="Aide pour l'orientation",
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        copy=False,
        default='new',
        selection=[('new', 'New'), ('offer', 'Offer'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')]
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    tags_id = fields.Many2many("estate.property.tag", string="Tags")
    # offer_id = fields.Many2one("estate.property.offer")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        max = 0.0
        for r in self:
            for o in r.offer_ids:
                if max < o.price:
                    max = o.price
            r.best_price = max
        return True

    def action_sold(self):
        for record in self:
            if record.state != "canceled":
                record.state = 'sold'
            else:
                raise ValidationError(_('Canceled properties cannot be sold'))
        return True

    def action_cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise ValidationError(_('Solded properties cannot be cancel'))
        return True

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else None
        self.garden_orientation = 'north' if self.garden else None

    @api.constrains("selling_price")
    def _constrains_selling_price(self):
        for record in self:
            is_less_than_90 = float_compare(90.0, (100 * float(record.selling_price) / float(record.expected_price)), precision_digits=1)
            print("less than {}", is_less_than_90)
            if not float_is_zero(record.selling_price, precision_digits=2) and is_less_than_90:
                raise ValidationError("Blabla 90%")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'A property selling price must be positive.'),
    ]