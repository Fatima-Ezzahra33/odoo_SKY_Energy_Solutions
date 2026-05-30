# -*- coding: utf-8 -*-
from odoo import models, fields


class SkyCapteur(models.Model):
    _name = 'sky.capteur'
    _description = 'Capteur Physique'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'installation_id, name'

    name = fields.Char(
        string='Nom du capteur',
        required=True,
    )
    installation_id = fields.Many2one(
        comodel_name='sky.installation',
        string='Installation',
        required=True,
        ondelete='cascade',
    )
    serial_number = fields.Char(
        string='Numéro de série',
    )
    protocole = fields.Selection(
        selection=[
            ('modbus', 'Modbus'),
            ('mqtt', 'MQTT'),
            ('api', 'API'),
            ('manual', 'Manuel'),
        ],
        string='Protocole',
        default='manual',
    )
    type_capteur = fields.Selection(
        selection=[
            ('production', 'Production'),
            ('irradiation', 'Irradiation'),
            ('temperature', 'Température'),
            ('onduleur', 'Onduleur'),
        ],
        string='Type de capteur',
        required=True,
    )
    date_installation = fields.Date(
        string='Date d\'installation',
    )
    state = fields.Selection(
        selection=[
            ('active', 'Actif'),
            ('inactive', 'Inactif'),
            ('panne', 'En panne'),
        ],
        string='État',
        default='active',
        tracking=True,
    )
    lecture_ids = fields.One2many(
        comodel_name='sky.lecture',
        inverse_name='capteur_id',
        string='Lectures',
    )
