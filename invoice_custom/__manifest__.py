# -*- coding: utf-8 -*-
{
    'name': "invoice_custom",

    'summary': """
       des fonctionnalié  a ajouter au module facturation""",

    'description': """
        Calculer total des commandes par client
        Calcules=r les moyennes des notes et sections
    """,

    'author': "Syrine Riahi",
    'website': "Syrineriahi11@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','web_studio'],

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
