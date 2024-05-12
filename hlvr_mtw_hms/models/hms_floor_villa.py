from odoo import api, fields, models

class FloorVilla(models.Model):
    _name = 'hms.floor.villa'
    _inherit = ['mail.thread']
    _description = 'Floor and Villa Information'

    name = fields.Char(string='Name', track_visibility='onchange')
    code = fields.Char(string='Code', track_visibility='onchange')
    floor_villa = fields.Selection([
        ('floor', 'Floor'),
        ('villa', 'Villa')
    ], string='Floor or Villa', track_visibility='onchange')
    sequence = fields.Integer(string='Sequence', track_visibility='onchange')
    total_room = fields.Integer(string='Total Room', compute='_compute_total_room', track_visibility='onchange')
    room_ids = fields.One2many('hms.room', 'floor_villa_id', string='Room', track_visibility='onchange')
    status = fields.Selection([('available', 'Available'),
                               ('out_of_order', 'Out Of Order')], default='available', string='Status',
                              track_visibility='onchange')

    @api.depends('room_ids')
    def _compute_total_room(self):
        for rec in self:
            rec.total_room = len(rec.room_ids)

    def action_available(self):
        return self.write({'status': 'available'})

    def action_out_of_order(self):
        return self.write({'status': 'out_of_order'})

