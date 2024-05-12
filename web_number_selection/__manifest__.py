{
    'name': 'Web Number Selection',
    'version': '16.0.0.0',
    'category': 'Website',
    'license': 'AGPL-3',
    'description': """
Extension for Web Number Selection Field
========================================
This module provides a customizable number selection field for web forms. 
The number selection field allows users to input numeric values within a specified range. 
It includes features such as placeholder text, minimum and maximum value constraints, and step size for incrementing or decrementing the value. 
The field is styled with a modern and user-friendly design, enhancing the overall user experience. 
Developers can easily integrate and customize this field in their web applications to capture numerical data efficiently.

Code Usage
==========
<field name="testing" widget="number_selection_widget" options="{'step': 0.25, 'min': 0, 'max': 10}" />
    """,
    'author': 'Mingalar Sky Co., Ltd.',
    'website': 'https://www.mingalarsky.com',
    'depends': ['base', 'web'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'web_number_selection/static/src/css/*.css',
            'web_number_selection/static/src/js/*.js',
            'web_number_selection/static/src/xml/*.xml'
        ]
    },
    'installable': True,
    'active': False,
}