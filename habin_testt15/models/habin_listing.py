from odoo import models, fields

class HabinListing(models.Model):
    _name = 'habin.list'
    _description = 'Listing'

    host_id = fields.Many2one('habin.host', required=True)
    house_name = fields.Char(required=True)
    description = fields.Text()
    location = fields.Char()
    price_per_night = fields.Float()
    deposit = fields.Float()
    house_type = fields.Selection([
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('guesthouse', 'Guesthouse')
    ], string="House Type", default='house', required=True)

    availability_status = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('unavailable', 'Unavailable')
    ], string="Availability Status", default='available')

    image = fields.Binary("House Image", attachment=True)
    created_at = fields.Datetime(string="Created At", default=lambda self: fields.Datetime.now())