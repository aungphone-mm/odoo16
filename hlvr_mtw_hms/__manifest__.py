# -*- coding: utf-8 -*-
{
    'name': "Hotel Management System",

    'summary': """
        Hotel Management System""",

    'description': """
    """,

    'author': "Mingalar Sky Co., Ltd.",
    'website': "https://www.mingalarsky.com",
    'sequence': 2,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hotel Management System',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'account','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hms_floor_villa_views.xml',
        'views/hms_room_views.xml',
        'views/hms_room_rate_views.xml',
        'views/hms_transaction_views.xml',
        'views/hms_reservation_views.xml',
        'security/code_reservation.xml',
        'widzard/revenue_breakdown_widzard.xml',
        'widzard/hms_reservation_wizard.xml',
        'views/hms_guest_views.xml',
        'views/hms_folio_views.xml',
        'reports/custom_template.xml',
        'reports/reservation_report.xml',
        'views/menu.xml',
    ],

    'application': True
}
