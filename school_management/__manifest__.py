# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'School Management',
    'category': 'School',
    'summary': 'School Management',
    'description': "School Management",
    'version': '15.0.0',
    'sequence': 0,
    'depends': [
        'base',
        'stock',
        'sale_management',
        'contacts',
        'account',
        'website',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/school_management_view.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    'assets': {},
}
