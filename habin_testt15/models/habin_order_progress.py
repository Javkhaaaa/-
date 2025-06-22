from odoo import models, fields, api
from datetime import date

class HabinOrderProgress(models.Model):
    _name = 'habin.order.progress'
    _description = 'Order Progress'
    _auto = False  # Энэ нь Odoo-д хүснэгт үүсгэхгүй, харин SQL view ашиглана гэсэн үг

    order_detail_id = fields.Many2one('habin.order_detail', string="Order Detail", readonly=True)
    guest_id = fields.Many2one('habin.guest', string='Guest', readonly=True)
    listing_id = fields.Many2one('habin.list', string='Listing', readonly=True)
    check_in_date = fields.Date(readonly=True)
    check_out_date = fields.Date(readonly=True)
    total_price = fields.Float(readonly=True)
    # Үүнийг анхаар Graph гарч ирэхгүй байгаа нь шалтгаан бол progress_percent нь store=False гэж заасан учраас
    progress_percent = fields.Float(string="Progress", compute="_compute_progress", store=False)

    @api.depends('check_in_date', 'check_out_date')
    def _compute_progress(self):
        for rec in self:
            if rec.check_in_date and rec.check_out_date:
                total_days = (rec.check_out_date - rec.check_in_date).days
                passed_days = (date.today() - rec.check_in_date).days
                if total_days > 0:
                    progress = (passed_days / total_days) * 100
                    rec.progress_percent = min(100, max(0, progress))
                else:
                    rec.progress_percent = 0
            else:
                rec.progress_percent = 0

    def init(self):
        # SQL VIEW үүсгэж байна
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW habin_order_progress AS (
                SELECT
                    od.id AS id,
                    od.id AS order_detail_id,
                    od.guest_id,
                    od.listing_id,
                    od.check_in_date,
                    od.check_out_date,
                    od.total_price
                FROM habin_order_detail od
            )
        """)
