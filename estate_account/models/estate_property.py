from odoo import models

class EstateAccountModel(models.Model):
    _inherit = "estate.property"
    def action_sold(self):
        print("ICI ON SOLD MDRR")
        journal = self.env['account.move'].sudo().with_context(default_move_type='out_invoice')._get_default_journal()
        val_invoice = {
            'journal_id': journal.id,
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                (
                    0,
                    0,
                    {
                        'name': "Selling Price",
                        'quantity': "1",
                        'price_unit': self.selling_price * 0.06
                    }
                ),
                (
                    0,
                    0,
                    {
                        'name': "Additionnal administrative feeds",
                        'quantity': "1",
                        'price_unit': 100.0
                    }
                ),
            ]
        }
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(val_invoice)
        print("ICI ON EST EN CREATE INVOICE")
        return super().action_sold()
