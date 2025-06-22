from odoo import models, fields, api

class HabinReview(models.Model):
    _name = 'habin.review'
    _description = 'Review'

    order_id = fields.Many2one('habin.orders', required=True)
    listing_id = fields.Many2one('habin.list', required=True)
    guest_id = fields.Many2one('habin.guest', required=True)

    
    review_star = fields.Selection([(str(i), str(i)) for i in range(1, 6)], required=True)
    review_text = fields.Text()
    created_at = fields.Datetime(default=fields.Datetime.now)

    guest_domain_id = fields.Integer(compute="_compute_domains", store=False)
    listing_domain_id = fields.Integer(compute="_compute_domains", store=False)
    
    @api.depends('order_id')
    def _compute_domains(self):
        for rec in self:
            rec.guest_domain_id = rec.order_id.guest_id.id if rec.order_id else False
            # Захиалгад хамаарах listing-г order_detail-оос авна
            order_detail = self.env['habin.order_detail'].search([('order_id', '=', rec.order_id.id)], limit=1)
            rec.listing_domain_id = order_detail.listing_id.id if order_detail else False