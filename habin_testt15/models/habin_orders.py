from odoo import models, fields

class HabinOrder(models.Model):
    _name = 'habin.orders'
    _description = 'Order'
    guest_id = fields.Many2one('habin.guest', required=True)
    created_at = fields.Datetime(default=fields.Datetime.now)
