from odoo import fields, models, api, exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "For the odoo tutorial"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_available = fields.Date(default=datetime.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    total_area = fields.Integer(compute="_compute_total_area")

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True,
        copy=False,
        default='new',
        compute="_copmute_state",
        store=True,
        readonly=False
    )

    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    type_id = fields.Many2one(
        "estate.property.type",
        string="Type",
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'Expected price must be non-negative'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be non-negative'
    )


    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_validity(self):
        for record in self:
            if record.selling_price != 0 and record.selling_price < record.expected_price * 0.9:
                raise exceptions.ValidationError("Selling price cannot be less than 90% of the expected price")

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        if self.state == 'offer_accepted':
            self.state = 'sold'
            return True
        else:
            return False
    
    def action_cancel(self):
        if self.state != 'sold':
            self.state = 'cancelled'
            return True
        else:
            return False
    

    @api.ondelete(at_uninstall=False)
    def delete(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise exceptions.UserError("Only properties in 'New' or 'Cancelled' state can be deleted.")