from odoo import api, fields, models

class ReservationReport(models.AbstractModel):
    _name = 'reservation.report'
    _description = 'Reservation Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hms.reservation'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'hms.reservation',
            'docs': docs,
        }