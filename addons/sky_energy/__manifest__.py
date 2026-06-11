# -*- coding: utf-8 -*-
{
    'name': 'Sky Energy Monitoring',
    'version': '1.0',
    'category': 'Operations/Energy',
    'summary': 'Module de supervision énergétique pour Sky Energy Solutions',
    'description': """
        Module custom Sky Energy ERP
        ============================
        Ce module permet de gérer :
        - Les installations solaires
        - Les capteurs physiques
        - Les lectures énergétiques
        - Les rendements
        - Les alertes métier
        - Les contrats de garantie énergétique
        - Les interventions de maintenance terrain
    """,
    'author': 'Sky Energy Solutions',
    'depends': ['base', 'mail'],
    'data': [
        'security/sky_energy_security.xml',
        'security/ir.model.access.csv',
        'data/sky_energy_sequence.xml',
        'views/sky_installation_views.xml',
        'views/sky_capteur_views.xml',
        'views/sky_lecture_views.xml',
        'views/sky_rendement_views.xml',
        'views/sky_alerte_views.xml',
        'views/sky_contrat_garantie_views.xml',
        'views/sky_intervention_views.xml',
        'views/sky_energy_menus.xml',  
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}