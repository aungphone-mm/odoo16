from odoo import fields, api, models

class Room(models.Model):
    _name = 'hms.room'
    _inherit = ['mail.thread']
    _inherits = {
        'product.product': 'product_id'
    }

    product_id = fields.Many2one(
        "product.product",
        "Product ID",
        required=True,
        delegate=True,
        ondelete="cascade",
    )
    sr_no = fields.Integer(string='No', compute='_get_line_no')
    floor_villa_id = fields.Many2one('hms.floor.villa', string='Floor or Villa')
    # name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    room_type = fields.Many2one('hms.room.type', string='Room Type')
    base_child = fields.Many2one('base.child', string="Base Child")
    description = fields.Text(string='Description')
    # status = fields.Many2one('hms.room.status', string="Room Status")
    room_category = fields.Many2one('hms.room.category', string="Room Category")
    room_images = fields.One2many('hms.room.line', 'room_image_id', string='Room Images', ondelete='cascade')
    # income_account_id = fields.Many2one('account.account', string='Income Account',
    #                                     domain=[('deprecated', '=', False)],
    #                                     help="This account will be used for invoices to value sales.")
    # expense_account_id = fields.Many2one('account.account', string='Expense Account',
    #                                      domain=[('deprecated', '=', False)],
    #                                      help="This account will be used for invoices to value expenses.")
    status = fields.Selection([
        ('available', 'Available'),
        ('dirty', 'Dirty'),
        ('occupied', 'Occupied')
    ], default='available', string='Status', track_visibility='onchange')

    def _get_line_no(self):
        for room in self.mapped('floor_villa_id'):
            sr_no = 1
            for room in room.room_ids:
                room.sr_no = sr_no
                sr_no += 1

class RoomStatus(models.Model):
    _name = 'hms.room.status'
    _description = "Room status Model"

    name = fields.Char("Name")

class RoomCategory(models.Model):
    _name = 'hms.room.category'
    _description = "Room Category Model"

    name = fields.Char("Name")

class RoomLine(models.Model):
    _name = 'hms.room.line'
    _description = 'Room Lines'

    name = fields.Char(string='Description')
    image = fields.Image(string='Image')
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now)
    room_image_id = fields.Many2one('hms.room', string='Room', ondelete='cascade')

class RoomType(models.Model):
    _name = 'hms.room.type'
    _inherit = ['mail.thread']
    _description = 'hms.room.type'

    name = fields.Char(string='Name')
    code1 = fields.Char(string='Code')
    total_rooms = fields.Integer('Total Rooms', compute='_compute_total_rooms')
    room_type_line_ids = fields.One2many('hms.room.rate.line', 'room_type', string='Room Type Lines')
    room_ids = fields.One2many('hms.room', 'room_type', string='Room')
    base_adult = fields.Integer(string="Base Adult")
    base_child = fields.Integer(string="Base Child")
    max_adult = fields.Integer(string="Max Adult")
    max_child = fields.Integer(string="Max Child")
    sequence = fields.Integer(string="Sequence")
    color = fields.Char(string='Color', default='#FFFFFF', widget='color')

    @api.depends('name')
    def _compute_total_rooms(self):
        for record in self:
            room_count = self.env['hms.room'].search_count([('room_type', '=', record.id)])
            record.total_rooms = room_count