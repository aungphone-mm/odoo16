from datetime import datetime

from odoo import fields, models


class Rate(models.Model):
    _name = 'hms.room.rate'
    _inherit = ['mail.thread']
    _description = 'Rate'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    floor_villa = fields.Char(string='Floor Or Villa')
    from_date = fields.Date(string='From Date', default=datetime.now())
    to_date = fields.Date(string='To Date')
    hours = fields.Boolean(string='Hours')
    hours_day = fields.Integer(string='Hours/Days')
    weekend = fields.Boolean(string='Weekend?')
    rate_ids = fields.One2many('hms.room.rate.line', 'rate_id', string='Rate')
    description = fields.Text(string='Description')


class RateLine(models.Model):
    _name = 'hms.room.rate.line'
    _inherit = ['mail.thread']
    _description = 'RateLine'

    name = fields.Char("Name", related='rate_id.name')
    rate_id = fields.Many2one('hms.room.rate', string='Rate')
    room_type = fields.Many2one('hms.room.type', string='Room Type')
    currency = fields.Many2one('res.currency', string='Currency')
    amount = fields.Float('Amount')

    def set_revenue(self):
        existing_records = self.env['revenue.breakdown.widzard'].search([('revenue_id', '=', self.id)])
        if existing_records:
            action = {
                'type': 'ir.actions.act_window',
                'res_model': 'revenue.breakdown.widzard',
                'view_mode': 'form',
                'res_id': existing_records[0].id,
                'context': {
                    'default_revenue_id': self.id,
                    'create': False,
                    'edit': False,
                }
            }
        else:
            action = {
                'type': 'ir.actions.act_window',
                'res_model': 'revenue.breakdown.widzard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_revenue_id': self.id,
                }
            }
        return action
