from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HabinOrderCreateWizard(models.TransientModel):
    _name = 'habin.order.create.wizard'
    _description = 'Create Order and Order Detail Wizard'

    guest_id = fields.Many2one('habin.guest', string="Guest", required=True)

    price_from = fields.Float(string="Min Price")
    price_to = fields.Float(string="Max Price")

    house_type = fields.Selection([
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('guesthouse', 'Guesthouse')
    ], string="House Type")

    listing_id = fields.Many2one(
        'habin.list',
        string="Listing",
        domain="['&', ('price_per_night', '>=', price_from), ('price_per_night', '<=', price_to), ('house_type', '=', house_type)]",
        required=True
    )

    check_in_date = fields.Date(required=True)
    check_out_date = fields.Date(required=True)

    @api.constrains('check_in_date', 'check_out_date')
    def _check_dates(self):
        for rec in self:
            if rec.check_out_date < rec.check_in_date:
                raise ValidationError("Check-out date must be after check-in date.")

    @api.onchange('price_from', 'price_to', 'house_type')
    def _onchange_filters(self):
        # When any filter changes, reset listing_id so user must re-select from filtered list
        self.listing_id = False

    def action_create_order(self):
        order = self.env['habin.orders'].create({
            'guest_id': self.guest_id.id
        })

        self.env['habin.order_detail'].create({
            'order_id': order.id,
            'listing_id': self.listing_id.id,
            'guest_id': self.guest_id.id,
            'check_in_date': self.check_in_date,
            'check_out_date': self.check_out_date
        })

        return {'type': 'ir.actions.act_window_close'}
