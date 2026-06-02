# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SkyInstallation(models.Model):
    _name = 'sky.installation'
    _description = 'Installation Solaire'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_mise_service desc, name'

    name = fields.Char(
        string='Nom de l\'installation',
        required=True,
        tracking=True,
    )
    reference = fields.Char(
        string='Référence',
        readonly=True,
        copy=False,
        default='Nouveau',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=True,
        tracking=True,
    )
    puissance_crete = fields.Float(
        string='Puissance crête (kWc)',
        digits=(10, 3),
    )
    orientation = fields.Selection(
        selection=[
            ('nord', 'Nord'),
            ('sud', 'Sud'),
            ('est', 'Est'),
            ('ouest', 'Ouest'),
            ('sud_est', 'Sud-Est'),
            ('sud_ouest', 'Sud-Ouest'),
        ],
        string='Orientation',
    )
    inclinaison = fields.Float(
        string='Inclinaison (°)',
    )
    date_mise_service = fields.Date(
        string='Date de mise en service',
        tracking=True,
    )
    localisation = fields.Char(
        string='Localisation',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('active', 'Active'),
            ('maintenance', 'En maintenance'),
            ('stopped', 'Arrêtée'),
        ],
        string='Statut',
        default='draft',
        tracking=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    # Relations
    capteur_ids = fields.One2many(
        comodel_name='sky.capteur',
        inverse_name='installation_id',
        string='Capteurs',
    )
    lecture_ids = fields.One2many(
        comodel_name='sky.lecture',
        inverse_name='installation_id',
        string='Lectures',
    )
    rendement_ids = fields.One2many(
        comodel_name='sky.rendement',
        inverse_name='installation_id',
        string='Rendements',
    )
    alerte_ids = fields.One2many(
        comodel_name='sky.alerte',
        inverse_name='installation_id',
        string='Alertes',
    )
    intervention_ids = fields.One2many(
        comodel_name='sky.intervention',
        inverse_name='installation_id',
        string='Interventions',
    )

    # Compteurs pour les smart buttons
    capteur_count = fields.Integer(compute='_compute_counts', string='Capteurs')
    lecture_count = fields.Integer(compute='_compute_counts', string='Lectures')
    alerte_count = fields.Integer(compute='_compute_counts', string='Alertes')
    intervention_count = fields.Integer(compute='_compute_counts', string='Interventions')

    @api.depends('capteur_ids', 'lecture_ids', 'alerte_ids', 'intervention_ids')
    def _compute_counts(self):
        for rec in self:
            rec.capteur_count = len(rec.capteur_ids)
            rec.lecture_count = len(rec.lecture_ids)
            rec.alerte_count = len(rec.alerte_ids)
            rec.intervention_count = len(rec.intervention_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'Nouveau') == 'Nouveau':
                vals['reference'] = self.env['ir.sequence'].next_by_code('sky.installation') or 'Nouveau'
        return super().create(vals_list)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_set_maintenance(self):
        self.write({'state': 'maintenance'})

    def action_stop(self):
        self.write({'state': 'stopped'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})
