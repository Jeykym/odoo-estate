from odoo import fields, models, api, exceptions
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "For the odoo tutorial"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[('pending', 'Pending'), ('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
        default='pending'
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one(
        related="property_id.type_id",
        store=True
    )

    _check_price = models.Constraint(
        'CHECK(price >= 0)',
        'Price must be non-negative'
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
    

    def action_accept(self):
        if self.status == 'pending' and self.property_id.state != 'offer_accepted':
            self.status = 'accepted'
            self.property_id.state = 'offer_accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            
            return True

        return False

    def action_refuse(self):
        if self.status == 'pending':
            self.status = 'refused'
            return True

        return False

    @api.model
    def create(self, vals):
        target_property = self.env['estate.property'].browse(vals[0]['property_id'])
        if target_property.offer_ids:
            min_offer = min(target_property.offer_ids.mapped('price'))
            if vals[0]['price'] < min_offer:
                raise exceptions.ValidationError("New offer's price must be equal to or higher than existing offers.")
        if target_property.state == 'new':
            target_property.state = 'offer_received'
        return super().create(vals)