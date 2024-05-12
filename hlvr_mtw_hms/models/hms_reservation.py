from odoo import api, fields, models
from datetime import datetime, timedelta, date
import datetime
from odoo.tools.translate import _

class Reservation(models.Model):
    _name = 'hms.reservation'
    _inherit = ['mail.thread']
    _description = "Reservation"

    name = fields.Char(string='Reservation No.', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    date = fields.Datetime(string="", default=lambda self: fields.Datetime.now())
    guest_id = fields.Many2one("res.partner", string="Guest Name")
    identification = fields.Char(string="Indentification")
    reserv_line_id = fields.One2many("hms.reservation.line", 'reserv_id', string="Reservation Line", ondelete='cascade')
    reserv_room_line_id = fields.One2many("hms.reservation.room.line", 'reserv_line_id', string="Room",
                                          ondelete='cascade')
    note = fields.Text(string="Note")
    nrc_no = fields.Char(string='NRC', required=False, related="guest_id.nrc_no")
    nrc_number = fields.Many2one('hms.guest.nrc.number', related="guest_id.nrc_number", string='')
    nrc_code = fields.Many2one('hms.guest.nrc.type', string='', related="guest_id.nrc_code", )
    nrc_desc = fields.Many2one('hms.guest.nrc.description', string='', related="guest_id.nrc_desc", )
    identification_type = fields.Char()
    company_id = fields.Many2one('res.partner', related="guest_id.parent_id")
    source_business = fields.Many2one('hms.guest.business.source')
    agent_id = fields.Many2one('res.partner', string='Agent', domain="[('agent', '=', True)]")

    deposit = fields.Boolean('Deposit?')
    room_id = fields.Many2one('hms.room', string='Room')
    status = fields.Selection([('draft', 'Draft'),
                               ('confirmed', 'Confirmed'),('cancel', 'Cancel')], default='draft', string='Status',
                              track_visibility='onchange')
    rate = fields.Many2one('hms.room.rate', string="Rate")

    def action_cancel(self):
        self.ensure_one()
        if self.reserv_room_line_id.room:
            self.reserv_room_line_id.room.write({'status': 'available'})
        self.write({'status': 'cancel'})

    def action_confirmed(self):
        self.ensure_one()
        if self.reserv_room_line_id.room:
            self.reserv_room_line_id.room.write({'status': 'occupied'})
        self.write({'status': 'confirmed'})

    def action_reset(self):
        self.ensure_one()
        if self.reserv_room_line_id.room:
            self.reserv_room_line_id.room.write({'status': 'available'})
        self.write({'status': 'draft'})

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq = self.env['ir.sequence'].next_by_code('hms.reservation')
            year = str(date.today().year)
            month = str(date.today().month).zfill(2)
            vals['name'] = f'REV/{year}/{month}/{seq:06}'
        res = super(Reservation, self).create(vals)
        return res

    def register_payment(self):
        print('Htun lin Aung')

    def find_free_rooms(self):
        for record in self:
            record.reserv_room_line_id = [(5, 0, 0)]
            lines_to_add = []
            for line in record.reserv_line_id:
                new_line = record.reserv_room_line_id.new({
                    'room_type': line.room_type,
                    'arrival_at': line.arrival_at,
                    'depart_at': line.depart_at,
                    'guest': line.guest,
                })
                lines_to_add.append((0, 0, new_line._convert_to_write(new_line._cache)))
            record.write({'reserv_room_line_id': lines_to_add})
            # raise UserError("Rooms are not available")

        unreserved = self.env['hms.reservation.room.line'].search(
            [('reserv_line_id', 'in', self.ids), ('room', 'in', ['', False])])
        # print(unreserved,"free room by id aung phone")
        for unreserved_line in unreserved:
            Room = self.env['hms.room']
            Reservation = self.env['hms.reservation.room.line']
            all_rooms = Room.search([]).mapped('id')
            res_rooms = Reservation.search([]).mapped('room')
            reserved_rooms = []
            for x in res_rooms:
                reserved_rooms.append(x.id)
            unreserved_rooms = set(all_rooms) - set(reserved_rooms)
            for room_id in unreserved_rooms:
                room_records = self.env['hms.room'].search(
                    [('room_type', '=', unreserved_line.room_type.id), ('id', '=', room_id)])
                if room_records:
                    unreserved_line.room = room_records.id
                    room_records.status = 'occupied'


            for price in unreserved_rooms:
                guestprice = self.env['hms.room.rate.line'].search(
                    [('room_type', '=', unreserved_line.room_type.id), ('rate_id', '=', self.guest_id.rate.id)])
                if guestprice:
                    unreserved_line.price = guestprice.amount
                    break
                else:
                    businessprice = self.env['hms.room.rate.line'].search(
                        [('room_type', '=', unreserved_line.room_type.id),
                         ('rate_id', '=', self.source_business.rate.id)])
                    if businessprice:
                        unreserved_line.price = businessprice.amount
                        break
                    else:
                        agentprice = self.env['hms.room.rate.line'].search(
                            [('room_type', '=', unreserved_line.room_type.id), ('rate_id', '=', self.agent_id.rate.id)])
                        if agentprice:
                            unreserved_line.price = agentprice.amount
                            break
                mainrate = self.env['hms.room.rate.line'].search(
                    [('room_type', '=', unreserved_line.room_type.id), ('rate_id', '=', self.rate.id)])
                if mainrate:
                    unreserved_line.price = mainrate.amount
                    break

        for line in self.reserv_room_line_id:
            guestrate = self.env['hms.room.rate'].search([('id', '=', self.guest_id.rate.id)])
            if guestrate:
                line.rate = guestrate.id
            else:
                businessrate = self.env['hms.room.rate'].search([('id', '=', self.source_business.rate.id)])
                if businessrate:
                    line.rate = businessrate.id
                else:
                    agentrate = self.env['hms.room.rate'].search([('id', '=', self.agent_id.rate.id)])
                    if agentrate:
                        line.rate = agentrate.id
            mainrate = self.env['hms.room.rate'].search([('id', '=', self.rate.id)])
            if mainrate:
                line.rate = mainrate.id

        wizard_form = self.env.ref('hlvr_mtw_hms.reservation_wizard_form_view')
        room_line_data = [
            (0, 0, {
                'room': room.room.id,
                'room_type': room.room_type.id,
                'guest': room.guest,
            }) for room in self.reserv_room_line_id
        ]
        wizard = self.env['hms.reservation.wizard'].create({
            'room_line_ids': room_line_data,
            'reservation_ids': [(6, 0, self.ids)]
        })
        return {
            'name': 'Reservation Wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hms.reservation.wizard',
            'views': [(wizard_form.id, 'form')],
            'view_id': wizard_form.id,
            'target': 'new',
            'res_id': wizard.id,
            'context': {
                'create': False,
                'edit': False,
            }
        }

class ReservationLine(models.Model):
    _name = 'hms.reservation.line'
    _description = "Reservation Line"

    # room = fields.Char("Room")
    room_type = fields.Many2one("hms.room.type", string="Room Type")
    guest = fields.Integer("Guest", track_visibility='onchange')
    arrival_at = fields.Datetime(default=lambda self: fields.Datetime.now())
    depart_at = fields.Datetime(string="Departure at",required=True)
    reserv = fields.Char("Reservation %")
    rate = fields.Many2one("hms.room.rate")
    breakfast = fields.Boolean("Breakfast")
    reserv_id = fields.Many2one("hms.reservation", string="Reservation", ondelete='cascade')
    guest_contact_id = fields.Many2one('res.partner')

class ReservationRoomLine(models.Model):
    _name = 'hms.reservation.room.line'
    _description = "Reservation Room Line"

    room = fields.Many2one("hms.room", string="Room")
    room_type = fields.Many2one("hms.room.type", string="Room Type")
    floorVilla = fields.Many2one("floor_villa", string="Floor or Villa")
    guest = fields.Integer("Guest", track_visibility='onchange')
    arrival_at = fields.Datetime(default=lambda self: fields.Datetime.now())
    depart_at = fields.Datetime(string="Departure at")
    rate = fields.Many2one("hms.room.rate")
    reserv_line_id = fields.Many2one("hms.reservation", string="Reservation", ondelete='cascade')
    night = fields.Integer("Night", compute='_compute_total_nights')
    price = fields.Float(compute='_compute_price', store=True)
    subtotal = fields.Char("Subtotal")
    guest_id = fields.Many2one('res.partner', related="reserv_line_id.guest_id")

    @api.depends('reserv_line_id.rate')
    def _compute_price(self):
        for line in self:
            line._update_price_from_rate()

    def _update_price_from_rate(self):
        if self.reserv_line_id.rate:
            matching_rate_line = next(
                (rl for rl in self.reserv_line_id.rate.rate_ids if rl.room_type == self.room_type), None)
            if matching_rate_line:
                self.price = matching_rate_line.amount
                self.rate = self.reserv_line_id.rate
            else:
                self.price = 0.0
                self.rate=''
        else:
            self.price = 0.0
            self.rate=''

    def _inverse_price(self):
        pass  # No need for inverse logic for price field

    @api.depends('reserv_line_id.rate')
    def _compute_rate(self):
        for line in self:
            line.rate = line.reserv_line_id.rate

    def _inverse_rate(self):
        for line in self:
            line._update_price_from_rate()

    @api.onchange('room_type')
    def _compute_selection(self):
        if self.room_type:
            # customerrate = self.env['hms.room.rate'].search([('id', '=', self.reserv_line_id.guest_id.rate.id)])
            # if not customerrate:
            #     return {'domain': {'rate': []}}
            return {'domain': {'room': [('id', '=', self.room_type.id)]}}
        else:
            return {'domain': {'room': []}}

    @api.depends('arrival_at', 'depart_at')
    def _compute_total_nights(self):
        for rec in self:
            if rec.arrival_at and rec.depart_at:
                start_date = fields.Datetime.from_string(rec.arrival_at)
                end_date = fields.Datetime.from_string(rec.depart_at)
                dif_nights = (end_date - start_date).days
                rec.night = dif_nights
            else:
                rec.night = 0
