import logging

from odoo import models, api, fields
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class RevenueBreakDown(models.TransientModel):
    _name = 'revenue.breakdown.widzard'
    _description = 'Revenue Break Down'

    revenue_id = fields.Many2one('hms.room.rate.line')
    line_ids = fields.One2many('revenue.breakdown.widzard.line', 'line_id')

    def save_revenue_data(self):
        for wizard_line in self:
            rate_line = wizard_line.revenue_id
            rate_amount = rate_line.amount
            if not rate_amount:
                raise UserError("Amount is not set in Rate Line.")

            total_line_amount = sum(line.amount for line in wizard_line.line_ids)
            if total_line_amount > rate_amount:
                raise ValidationError("Total amount cannot exceed the rate line amount.")
            else:
                _logger.info("Total amount does not exceed the rate line amount.")

    @api.onchange('line_ids')
    def _onchange_line_ids(self):
        for line in self.line_ids:
            line.amount = ((line.percentage / 100.0) * self.revenue_id.amount) * 100


class RevenueBreakDownLine(models.TransientModel):
    _name = 'revenue.breakdown.widzard.line'

    line_id = fields.Many2one('revenue.breakdown.widzard')
    transaction_code_id = fields.Many2one('hms.transaction', 'Transaction Code')
    account = fields.Many2one('account.account', 'Account', related='transaction_code_id.account')
    percentage = fields.Float('Percentage')
    currency_id = fields.Many2one('res.currency', string='Currency')
    amount = fields.Integer('Amount')
