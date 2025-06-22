from odoo import models, fields

class HabinPayment(models.Model):
    _name = 'habin.payment'
    _description = 'Payment'

    order_id = fields.Many2one('habin.orders', required=True)
    
    payment_method = fields.Selection([
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('paypal', 'PayPal')
    ], string="Payment Method", default='card')

    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('failed', 'Failed')
    ], string="Payment Status", default='pending')

    created_at = fields.Datetime(string="Created At", default=lambda self: fields.Datetime.now())
