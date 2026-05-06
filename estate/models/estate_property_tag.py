from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "For the odoo tutorial"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _check_name = models.Constraint(
        'UNIQUE(name)',
        "Tag's name must be unique"
    )