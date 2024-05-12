from odoo import fields, models


class Transaction(models.Model):
    _name = 'hms.transaction'
    _inherit = ['mail.thread']
    _description = 'Transaction'

    name = fields.Char(string='Code')
    desc = fields.Char(string='Description')
    category = fields.Char(string='Category')
    account = fields.Many2one('account.account', string='Account')
    tax = fields.Many2many('account.tax', string='Tax')
    sequence = fields.Char(string='Sequence')
