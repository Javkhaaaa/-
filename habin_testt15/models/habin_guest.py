from odoo import models, fields, api

class HabinGuest(models.Model):
    _name = 'habin.guest'
    _description = 'Guest'
    guest_fname = fields.Char(required=True)
    guest_lname = fields.Char(required=True)
    gender = fields.Selection([
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
    ], string="Gender")
    guest_email = fields.Char()
    guest_phoneNumber = fields.Char()
    created_at = fields.Datetime(default=fields.Datetime.now)
    name = fields.Char(compute='_compute_name', store=True)

    @api.depends('guest_fname', 'guest_lname')
    def _compute_name(self):
        for r in self:
            r.name = f"{r.guest_fname} {r.guest_lname}"
