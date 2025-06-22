from odoo import models, fields, api

class HabinHost(models.Model):
    _name = 'habin.host'
    _description = 'Host'
    host_fname = fields.Char(required=True)
    host_lname = fields.Char(required=True)
    gender = fields.Selection([
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
    ], string="Gender")
    host_email = fields.Char()
    host_phoneNumber = fields.Char()
    created_at = fields.Datetime(default=fields.Datetime.now)
    name = fields.Char(compute='_compute_name', store=True)

    @api.depends('host_fname', 'host_lname')
    def _compute_name(self):
        for r in self:
            r.name = f"{r.host_fname} {r.host_lname}"
