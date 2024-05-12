from odoo import models, fields, api


class Guest(models.Model):
    _inherit = 'res.partner'

    business_source = fields.Many2one('hms.guest.business.source')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender",
                              )
    birth_date = fields.Date(string="Birth Date")
    id_type = fields.Many2one('hms.guest.identification.type', 'ID Type')
    # NRC Section
    nrc_no = fields.Char(string='NRC')
    nrc_number = fields.Many2one('hms.guest.nrc.number')
    nrc_code = fields.Many2one('hms.guest.nrc.type')
    nrc_desc = fields.Many2one('hms.guest.nrc.description')
    father_name = fields.Char(string="Father Name")
    race = fields.Char(string="Race")
    profession = fields.Char(string="Profession")
    nationality = fields.Many2one('hms.guest.nationality', string="Nationality")
    postcode = fields.Char(string="Postcode")
    immigration_remark = fields.Text(string="Immigration Remark")
    religion = fields.Char(string="Religion")
    remark = fields.Text(string="Remark")
    current_room = fields.Many2one('hms.room', string="Current room")
    reservation_room_line_ids = fields.One2many('hms.reservation.room.line', 'guest_id', string="Reservation History")
    rate = fields.Many2one('hms.room.rate', string="Rate")
    agent = fields.Boolean('Agent?')

    @api.onchange('nrc_number')
    def onchange_nrc_number(self):
        if self.nrc_number and self.nrc_number.id:
            return {'domain': {'nrc_desc': [('parent_id', '=', self.nrc_number.id)]}}
        else:
            return {'domain': {'nrc_desc': []}}


class Nationality(models.Model):
    _name = "hms.guest.nationality"
    _description = "Nationality"
    _rec_name = "nationality"
    _order = "sequence"

    sequence = fields.Integer(string="Sequence")
    nationality = fields.Char(string="Nationality", store=True)
    nationality_code = fields.Char(string="Nationality Code")


class IdentificationType(models.Model):
    _name = "hms.guest.identification.type"
    _description = "Identification Type"

    name = fields.Char('Name')


    # NRC start


class NRCDescription(models.Model):
    _name = "hms.guest.nrc.description"
    _order = 'name asc'

    name = fields.Char('Name', required=True)
    parent_id = fields.Many2one('hms.guest.nrc.number', 'Parent')


class NRCNUmber(models.Model):
    _name = "hms.guest.nrc.number"

    name = fields.Char('Number', required=True)


class NRCType(models.Model):
    _name = "hms.guest.nrc.type"

    name = fields.Char('Type', required=True)
    # NRC end


class SourceBusiness(models.Model):
    _name = "hms.guest.business.source"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code')
    description = fields.Text('Description')
    rate = fields.Many2one('hms.room.rate', string="Rate")

