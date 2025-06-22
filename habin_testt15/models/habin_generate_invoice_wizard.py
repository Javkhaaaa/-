# models/habin_generate_invoice_wizard.py
from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import tempfile
import os

class HabinGenerateInvoiceWizard(models.TransientModel):
    _name = 'habin.generate.invoice.wizard'
    _description = 'Generate Invoice and Send Email'

    order_detail_id = fields.Many2one('habin.order_detail', string='Order Detail', required=True)
    additional_notes = fields.Text(string="Additional Notes")
    send_email = fields.Boolean(string="Send to Guest Email", default=True)

    def action_generate_invoice(self):
        self.ensure_one()
        order = self.order_detail_id

        # PDF тайланг render хийх
        pdf = self.env.ref('habin_testt15.action_invoice_pdf_template')._render_qweb_pdf(order.id)[0]
        filename = f"Invoice_{order.id}.pdf"
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(pdf),
            'res_model': 'habin.order_detail',
            'res_id': order.id,
            'mimetype': 'application/pdf'
        })

        if self.send_email:
            if not order.guest_id.email:
                raise UserError("Guest email is missing.")

            template = self.env.ref('habin_testt15.email_template_invoice_send')
            template.attachment_ids = [(6, 0, [attachment.id])]
            template.send_mail(order.id, force_send=True)

        return {
            'type': 'ir.actions.act_window_close'
        }
