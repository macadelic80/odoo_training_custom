from odoo import models, fields, api


class EstateOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float(default=0.0)
    status = fields.Selection(
        copy=True,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Proprety", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(default=fields.Date.today(), compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        print("JE INVERSE DEADLINE")
        for record in self:
            record.validity = fields.Date.subtract(record.date_deadline, days=fields.Date.today().day).day
            # print("ICIII {} - {}".format(record.date_deadline, fields.Date.today()))
