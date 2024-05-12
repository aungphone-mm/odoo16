from odoo import api, fields, models, _

class HMSFolio(models.Model):
    _name = 'hms.folio'
    _inherit = ['mail.thread']
    _description = 'Folio'

    name = fields.Char('Folio No', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    guest_id = fields.Many2one("res.partner", string="Guest Name", track_visibility='onchange',)
    reservation_no = fields.Many2one('hms.reservation', 'Reservation No')
    nrc_no = fields.Char(string='NRC', required=False, related="guest_id.nrc_no")
    nrc_number = fields.Many2one('hms.guest.nrc.number', related="guest_id.nrc_number", string='')
    nrc_code = fields.Many2one('hms.guest.nrc.type', string='', related="guest_id.nrc_code", )
    nrc_desc = fields.Many2one('hms.guest.nrc.description', string='', related="guest_id.nrc_desc", )
    identification_type = fields.Many2one(related="guest_id.id_type")
    rate = fields.Many2one('hms.room.rate', track_visibility='onchange', related="guest_id.rate")
    main_folio_no = fields.Char('Main Folio No')
    room = fields.Many2one('hms.room', track_visibility='onchange')
    room_type = fields.Many2one('hms.room.type', track_visibility='onchange')
    floor_villa_id = fields.Many2one('hms.floor.villa', string='Floor or Villa', track_visibility='onchange')
    total_guests = fields.Integer(string='Total Guests', track_visibility='onchange', compute='_compute_total_guest')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, track_visibility='onchange')
    business_source = fields.Many2one('hms.guest.business.source', track_visibility='onchange', related="guest_id.business_source")
    agent_id = fields.Many2one('res.partner', string='Agent')
    deposit = fields.Boolean('Deposit?')
    amount_due = fields.Integer('Amount Due')
    main_folio = fields.Boolean('Main Folio')
    arrival_at = fields.Datetime('Arrival At', default=lambda self: fields.Datetime.now())
    departure_at = fields.Datetime(string="Departure At")
    total_day = fields.Integer('Total Day(s)', compute='_compute_total_days')
    related_folios = fields.Integer('Related Folios', compute='_compute_related_folios')

    status = fields.Selection([('confirm', 'Confirm'),
                               ('check_in_out', 'Check In/Out')], default='confirm', string='Status',
                              track_visibility='onchange')
    folio_ids = fields.One2many('hms.folio.line', 'folio_id', 'Folio Id')

    # @api.onchange('reservation_no')
    # def _onchange_reservation_no(self):
    #     if self.reservation_no and self.reservation_no.reserv_room_line_id:
    #         self.guest_id = self.reservation_no.guest_id.id
    #         self.room_type = self.reservation_no.reserv_room_line_id[0].room_type.id
    #         room1 = self.reservation_no.reserv_room_line_id[0].room
    #         if room1 and isinstance(room1, str):
    #             # If room1 is a string, find the room object by its name
    #             room_obj = self.env['hms.reservation.room.line'].search([('room', '=', room1)], limit=1)
    #             if room_obj:
    #                 self.room = room_obj.id
    #         elif room1:
    #             # If room1 is already a room object, assign its id directly
    #             self.room = room1.id
    def action_confirm(self):
        return self.write({'status': 'check_in_out'})

    def action_check_in_out(self):
        return self.write({'status': 'confirm'})

    @api.model
    def create(self, vals_list):
        if 'name' not in vals_list or vals_list.get('name') == 'New':
            vals_list['name'] = self.env['ir.sequence'].next_by_code('hms.folio') or 'New'
        return super(HMSFolio, self).create(vals_list)

    def register_payment(self):
        print('Htun lin Aung')

    @api.depends('arrival_at', 'departure_at')
    def _compute_total_days(self):
        for rec in self:
            if rec.arrival_at and rec.departure_at:
                start_date = fields.Datetime.from_string(rec.arrival_at)
                end_date = fields.Datetime.from_string(rec.departure_at)
                dif_days = (end_date - start_date).days
                rec.total_day = dif_days
            else:
                rec.total_day = 0

    @api.depends('folio_ids')
    def _compute_total_guest(self):
        for rec in self:
            rec.total_guests = len(rec.folio_ids)

    @api.depends('folio_ids')
    def _compute_related_folios(self):
        for rec in self:
            rec.related_folios = len(rec.folio_ids)
class HMSFolioLine(models.Model):
    _name = 'hms.folio.line'
    _inherit = ['mail.thread']
    _description = 'Folio Line'

    folio_id = fields.Many2one('hms.folio')
    line_name = fields.Char('Folio No', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    guest_id = fields.Many2one("res.partner", string="Guest Name", track_visibility='onchange')
    identification_type = fields.Many2one(related="guest_id.id_type", string='Identification Type')
    nrc_no = fields.Char(string='NRC', required=False, related="guest_id.nrc_no")
    nrc_number = fields.Many2one('hms.guest.nrc.number', related="guest_id.nrc_number", string='')
    nrc_code = fields.Many2one('hms.guest.nrc.type', string='', related="guest_id.nrc_code", )
    nrc_desc = fields.Many2one('hms.guest.nrc.description', string='', related="guest_id.nrc_desc", )
    rate = fields.Many2one('hms.room.rate', track_visibility='onchange', related="guest_id.rate")
    room = fields.Many2one('hms.room', track_visibility='onchange')
    room_type = fields.Many2one('hms.room.type', track_visibility='onchange')
    main_folio_no = fields.Char('Main Folio No', compute='compute_main_folio_no')
    identification_id = fields.Char(compute="_compute_identification_id")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, track_visibility='onchange')
    business_source = fields.Many2one('hms.guest.business.source', track_visibility='onchange',
                                      related="guest_id.business_source")
    agent_id = fields.Many2one('res.partner', string='Agent')
    deposit = fields.Boolean('Deposit?')
    amount_due = fields.Integer('Amount Due')
    main_folio = fields.Boolean('Main Folio')
    floor_villa_id = fields.Many2one('hms.floor.villa', string='Floor or Villa', track_visibility='onchange')
    arrival_at = fields.Datetime('Arrival At', default=lambda self: fields.Datetime.now())
    departure_at = fields.Datetime(string="Departure At")
    total_day = fields.Integer('Total Day(s)', compute='_compute_total_days')
    @api.depends('nrc_no', 'nrc_code', 'nrc_desc', 'nrc_number')
    def _compute_identification_id(self):
        for record in self:
            nrc_no = record.nrc_no or ''
            nrc_code = record.nrc_code.name if record.nrc_code else ''
            nrc_desc = record.nrc_desc.name if record.nrc_desc else ''
            nrc_number = record.nrc_number.name if record.nrc_number else ''
            identification_id = f"{nrc_number}{nrc_desc}{nrc_code}{nrc_no}"
            record.identification_id = identification_id

    @api.model
    def create(self, vals_list):
        if 'line_name' not in vals_list or vals_list.get('line_name') == 'New':
            vals_list['line_name'] = self.env['ir.sequence'].next_by_code('hms.folio') or 'New'
        return super(HMSFolioLine, self).create(vals_list)

    def compute_main_folio_no(self):
        for rec in self:
            rec.main_folio_no = self.folio_id.name

    @api.depends('arrival_at', 'departure_at')
    def _compute_total_days(self):
        for rec in self:
            if rec.arrival_at and rec.departure_at:
                start_date = fields.Datetime.from_string(rec.arrival_at)
                end_date = fields.Datetime.from_string(rec.departure_at)
                dif_days = (end_date - start_date).days
                rec.total_day = dif_days
            else:
                rec.total_day = 0

    def register_payment(self):
        print('Htun lin Aung')
