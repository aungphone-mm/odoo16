from odoo import models, fields, api

class ReservationWizard(models.TransientModel):
    _name = 'hms.reservation.wizard'

    # room_type = fields.Many2one("hms.room.type", string="Room Type")
    room_line_ids = fields.One2many('hms.reservation.room.line.wizard', 'wizard_id', string='Room Lines')
    reservation_ids = fields.Many2many('hms.reservation', string='Reservations')
    reservation_ids_text = fields.Char(compute='_compute_reservation_ids_text', string='Reservation IDs')
    room_lines_with_room = fields.One2many('hms.reservation.room.line.wizard', 'wizard_id',
                                           string='Room', domain=[('room', '!=', False)])
    room_lines_without_room = fields.One2many('hms.reservation.room.line.wizard', 'wizard_id',
                                              string='Room', domain=[('room', '=', False)])

    @api.depends('reservation_ids')
    def _compute_reservation_ids_text(self):
        for wizard in self:
            wizard.reservation_ids_text = ', '.join(str(reservation.id) for reservation in wizard.reservation_ids)

    def action_no_button(self):
        reservation_ids = self.reservation_ids.ids
        room_line_model = self.env['hms.reservation.room.line']
        room_lines = room_line_model.search([('reserv_line_id', 'in', reservation_ids)])
        room_lines.unlink()

        room_line_model1 = self.env['hms.reservation.wizard'].search([])
        room_line_model1.unlink()

        room_line_model1 = self.env['hms.reservation.room.line.wizard'].search([])
        room_line_model1.unlink()

    def action_continue_button(self):
        reservation_ids = self.reservation_ids.ids
        room_line_model = self.env['hms.reservation.room.line']
        room_lines = room_line_model.search([('reserv_line_id', 'in', reservation_ids), ('room', 'in', ['', False])])
        room_lines.unlink()

class ReservationRoomLineWizard(models.TransientModel):
    _name = 'hms.reservation.room.line.wizard'

    room = fields.Many2one("hms.room", string="Room")
    room_type = fields.Many2one("hms.room.type", string="Room Type")
    room_name = fields.Char(related='room.name', string='Room Name', readonly=True)
    room_type_name = fields.Char(related='room.room_type.name', string='Room Type', readonly=True)
    wizard_id = fields.Many2one('hms.reservation.wizard', string='Wizard')
    guest = fields.Integer("Guest")
    floorvilla = fields.Char(related='room.floor_villa_id.name', string='Floor/Villa', readonly=True)

    # @api.onchange('room')
    # def _onchange_room_id(self):
    #     if self.room:
    #         self.room_type = self.room.room_type.id
