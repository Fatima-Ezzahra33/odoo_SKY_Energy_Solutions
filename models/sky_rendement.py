# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SkyRendement(models.Model):
    _name = 'sky.rendement'
    _description = 'Rendement Énergétique'
    _order = 'periode_debut desc'

    name = fields.Char(
        string='Référence rendement',
        required=True,
    )
    installation_id = fields.Many2one(
        comodel_name='sky.installation',
        string='Installation',
        required=True,
        ondelete='cascade',
    )
    periode_debut = fields.Date(
        string='Début de période',
        required=True,
    )
    periode_fin = fields.Date(
        string='Fin de période',
        required=True,
    )
    energie_reelle_kwh = fields.Float(
        string='Énergie réelle (kWh)',
        digits=(10, 3),
    )
    energie_prevue_kwh = fields.Float(
        string='Énergie prévue (kWh)',
        digits=(10, 3),
    )
    performance_ratio = fields.Float(
        string='Performance Ratio (%)',
        compute='_compute_rendement',
        store=True,
        digits=(6, 2),
    )
    ecart_percent = fields.Float(
        string='Écart (%)',
        compute='_compute_rendement',
        store=True,
        digits=(6, 2),
    )
    state = fields.Selection(
        selection=[
            ('normal', 'Normal'),
            ('warning', 'Avertissement'),
            ('critical', 'Critique'),
        ],
        string='État',
        compute='_compute_rendement',
        store=True,
    )

    @api.depends('energie_reelle_kwh', 'energie_prevue_kwh')
    def _compute_rendement(self):
        for rec in self:
            if rec.energie_prevue_kwh and rec.energie_prevue_kwh > 0:
                pr = (rec.energie_reelle_kwh / rec.energie_prevue_kwh) * 100
                ecart = ((rec.energie_reelle_kwh - rec.energie_prevue_kwh) / rec.energie_prevue_kwh) * 100
                rec.performance_ratio = pr
                rec.ecart_percent = ecart
                if pr >= 90:
                    rec.state = 'normal'
                elif pr >= 75:
                    rec.state = 'warning'
                else:
                    rec.state = 'critical'
            else:
                rec.performance_ratio = 0.0
                rec.ecart_percent = 0.0
                rec.state = 'normal'
