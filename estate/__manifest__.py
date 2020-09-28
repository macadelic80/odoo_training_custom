
{
    'name': 'Estate',
    'version': '1.0',
    'author': "Achraf (abz)",
    'category': 'Immo',
    'summary': 'First app',
    'depends': ['web', 'base'],
    'description': "Immo app first",
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_tag_views.xml',
        'views/estate_user_view.xml',
        'views/estate_type_views.xml',
        'views/estate_menu.xml'
    ]
}
