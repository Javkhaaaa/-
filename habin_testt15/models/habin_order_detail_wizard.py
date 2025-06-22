from odoo import models, fields, api

class HabinOrderDetailReportWizard(models.TransientModel):
    _name = 'habin.order.detail.report.wizard'
    _description = 'Order Detail Report Wizard'

    guest_id = fields.Many2one('habin.guest', string="Guest", required=True)
    order_detail_ids = fields.One2many('habin.order_detail', compute='_compute_order_details', string="Order Details")

    @api.depends('guest_id')
    def _compute_order_details(self):
        for wizard in self:
            wizard.order_detail_ids = self.env['habin.order_detail'].search([
                ('guest_id', '=', wizard.guest_id.id)
            ])
