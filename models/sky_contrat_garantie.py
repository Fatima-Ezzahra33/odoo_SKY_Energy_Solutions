# -*- coding: utf-8 -*-
from odoo import models, fields


class SkyContratGarantie(models.Model):
    _name = 'sky.contrat.garantie'
    _description = 'Contrat de Garantie Énergétique'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_debut desc'

    name = fields.Char(
        string='Référence contrat',
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=True,
        tracking=True,
    )
    installation_id = fields.Many2one(
        comodel_name='sky.installation',
        string='Installation',
        required=True,
        tracking=True,
    )
    date_debut = fields.Date(
        string='Date de début',
        required=True,
    )
    date_fin = fields.Date(
        string='Date de fin',
        required=True,
    )
    energie_garantie_annuelle = fields.Float(
        string='Énergie garantie annuelle (kWh)',
        digits=(10, 3),
    )
    tolerance_percent = fields.Float(
        string='Tolérance (%)',
        digits=(5, 2),
        default=5.0,
    )
    penalite_percent = fields.Float(
        string='Pénalité (%)',
        digits=(5, 2),
        default=10.0,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('active', 'Actif'),
            ('expired', 'Expiré'),
            ('cancelled', 'Annulé'),
        ],
        string='État',
        default='draft',
        tracking=True,
    )

    def action_activate(self):
        self.write({'state': 'active'})

    def action_expire(self):
        self.write({'state': 'expired'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
