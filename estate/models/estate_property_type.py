from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "For the odoo tutorial"
    _order = "sequence, name"

    name = fields.Char(required=True)
    offer_count = fields.Integer(compute="_compute_offer_count")
    
    property_ids = fields.One2many("estate.property", "type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    

    sequence  = fields.Integer('Sequence', default=1, help="Used to order the types, the lower the better")
    
    _check_name = models.Constraint(
        'UNIQUE(name)',
        "Type's name must be unique"
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)