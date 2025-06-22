from odoo import models, fields, api

class HabinOrderDetail(models.Model):
    _name = 'habin.order_detail'
    _description = 'Order Detail'

    order_id = fields.Many2one('habin.orders', required=True)
    listing_id = fields.Many2one('habin.list', required=True)
    guest_id = fields.Many2one('habin.guest', required=True)
    check_in_date = fields.Date(required=True)
    check_out_date = fields.Date(required=True)
    total_days = fields.Integer(compute='_compute_days', store=True)
    
    guest_domain_id = fields.Integer(compute="_compute_guest_domain", store=False)
    
    @api.depends('order_id')
    def _compute_guest_domain(self):
        for rec in self:
            rec.guest_domain_id = rec.order_id.guest_id.id if rec.order_id else False

    @api.depends('check_in_date', 'check_out_date')
    def _compute_days(self):
        for r in self:
            if r.check_in_date and r.check_out_date:
                r.total_days = (r.check_out_date - r.check_in_date).days
            else:
                r.total_days = 0
                
    total_price = fields.Float(compute="_compute_total_price", store=True)

    @api.depends('total_days', 'listing_id')
    def _compute_total_price(self):
        for r in self:
            r.total_price = r.total_days * r.listing_id.price_per_night if r.listing_id else 0
