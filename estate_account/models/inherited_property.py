from odoo import models, fields

class InheritedProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        print("Inherited sold action called")
        return super().action_sold()