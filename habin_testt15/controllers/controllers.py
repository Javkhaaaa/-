from odoo import http
from odoo.http import request

class HabinApiController(http.Controller):

    @http.route('/api/order_progress', type='json', auth='user', methods=['POST'], csrf=False)
    def get_order_progress(self, **kwargs):
        order_detail_id = kwargs.get('order_detail_id')
        if not order_detail_id:
            return {"error": "order_detail_id is required"}

        order_progress = request.env['habin.order.progress'].search([('order_detail_id', '=', int(order_detail_id))], limit=1)
        if not order_progress:
            return {"error": "Order progress not found"}

        return {
            'order_detail_id': order_progress.order_detail_id.id,
            'guest': {
                'id': order_progress.guest_id.id,
                'name': order_progress.guest_id.name,
                'email': order_progress.guest_id.email,
            },
            'listing': {
                'id': order_progress.listing_id.id,
                'house_name': order_progress.listing_id.house_name,
                'price_per_night': order_progress.listing_id.price_per_night,
            },
            'check_in_date': str(order_progress.check_in_date),
            'check_out_date': str(order_progress.check_out_date),
            'total_price': order_progress.total_price,
            'progress_percent': order_progress.progress_percent,
        }

    @http.route('/api/guest/<int:guest_id>', type='json', auth='user', methods=['GET'])
    def get_guest_info(self, guest_id):
        guest = request.env['habin.guest'].browse(guest_id)
        if not guest.exists():
            return {"error": "Guest not found"}

        return {
            'id': guest.id,
            'name': guest.name,
            'email': guest.email,
            # энд guest model дахь бусад талбаруудыг нэмнэ
        }

    @http.route('/api/listing/<int:listing_id>', type='json', auth='user', methods=['GET'])
    def get_listing_info(self, listing_id):
        listing = request.env['habin.list'].browse(listing_id)
        if not listing.exists():
            return {"error": "Listing not found"}

        return {
            'id': listing.id,
            'house_name': listing.house_name,
            'address': listing.address,
            'price_per_night': listing.price_per_night,
            # бусад талбаруудыг нэмнэ
        }
