from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "For the odoo tutorial"
    _order = "sequence, name"

    name = fields.Char(required=True)
    
    property_ids = fields.One2many("estate.property", "type_id", string="Properties")

    sequence  = fields.Integer('Sequence', default=1, help="Used to order the types, the lower the better")
    
    _check_name = models.Constraint(
        'UNIQUE(name)',
        "Type's name must be unique"
    )