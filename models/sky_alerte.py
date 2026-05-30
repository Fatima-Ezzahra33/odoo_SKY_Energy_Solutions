# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SkyAlerte(models.Model):
    _name = 'sky.alerte'
    _description = 'Alerte Métier'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_alerte desc'

    name = fields.Char(
        string='Référence alerte',
        readonly=True,
        copy=False,
        default='Nouveau',
    )
    installation_id = fields.Many2one(
        comodel_name='sky.installation',
        string='Installation',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    type_alerte = fields.Selection(
        selection=[
            ('production_basse', 'Production basse'),
            ('capteur_panne', 'Capteur en panne'),
            ('temperature_haute', 'Température haute'),
            ('communication_perdue', 'Communication perdue'),
            ('autre', 'Autre'),
        ],
        string='Type d\'alerte',
        required=True,
    )
    date_alerte = fields.Datetime(
        string='Date de l\'alerte',
        required=True,
        default=fields.Datetime.now,
    )
    description = fields.Text(
        string='Description',
    )
    severity = fields.Selection(
        selection=[
            ('low', 'Faible'),
            ('medium', 'Moyen'),
            ('high', 'Élevé'),
            ('critical', 'Critique'),
        ],
        string='Sévérité',
        default='medium',
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('open', 'Ouverte'),
            ('in_progress', 'En cours'),
            ('resolved', 'Résolue'),
            ('cancelled', 'Annulée'),
        ],
        string='État',
        default='open',
        tracking=True,
    )
    intervention_id = fields.Many2one(
        comodel_name='sky.intervention',
        string='Intervention liée',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('sky.alerte') or 'Nouveau'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_resolve(self):
        self.write({'state': 'resolved'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_create_intervention(self):
        self.ensure_one()
        intervention = self.env['sky.intervention'].create({
            'name': self.env['ir.sequence'].next_by_code('sky.intervention') or 'Nouveau',
            'installation_id': self.installation_id.id,
            'alerte_id': self.id,
            'description': self.description or '',
            'type_intervention': 'corrective',
        })
        self.intervention_id = intervention
        self.state = 'in_progress'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Intervention',
            'res_model': 'sky.intervention',
            'res_id': intervention.id,
            'view_mode': 'form',
        }
