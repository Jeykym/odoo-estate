from odoo import models, fields, Command

class InheritedProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()

        for record in self:
           self.env['account.move'].create({
               'move_type': 'out_invoice',
               'partner_id': record.buyer_id.id,
               'line_ids': [
                    Command.create({
                        'name': 'Commision fee',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06
                    }),
                    Command.create({
                        'name': 'Administration fee',
                        'quantity': 1,
                        'price_unit': 100
                    })
               ]
           }) 

        return res