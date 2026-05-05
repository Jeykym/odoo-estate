from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "For the odoo tutorial"

    name = fields.Char(required=True)
    
    _check_name = models.Constraint(
        'UNIQUE(name)',
        "Type's name must be unique"
    )