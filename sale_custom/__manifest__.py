# -*- coding: utf-8 -*-
{
    'name': "sale_custom",

    'summary': """
       des fonctionnalié  a ajouter au module vente""",

    'description': """
        Calculer total des commandes par client
    """,

    'author': "SYRINE RIAHI",
    'website': "syrineriahi11@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
