# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SkyIntervention(models.Model):
    _name = 'sky.intervention'
    _description = 'Intervention Terrain'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_planifiee desc'

    name = fields.Char(
        string='Référence intervention',
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
    alerte_id = fields.Many2one(
        comodel_name='sky.alerte',
        string='Alerte liée',
    )
    technicien_id = fields.Many2one(
        comodel_name='res.users',
        string='Technicien',
        tracking=True,
    )
    date_planifiee = fields.Datetime(
        string='Date planifiée',
        tracking=True,
    )
    date_realisation = fields.Datetime(
        string='Date de réalisation',
    )
    type_intervention = fields.Selection(
        selection=[
            ('corrective', 'Corrective'),
            ('preventive', 'Préventive'),
            ('inspection', 'Inspection'),
        ],
        string='Type d\'intervention',
        required=True,
        default='corrective',
    )
    description = fields.Text(
        string='Description',
    )
    solution = fields.Text(
        string='Solution appliquée',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('planned', 'Planifiée'),
            ('done', 'Réalisée'),
            ('cancelled', 'Annulée'),
        ],
        string='État',
        default='draft',
        tracking=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('sky.intervention') or 'Nouveau'
        return super().create(vals_list)

    def action_plan(self):
        self.write({'state': 'planned'})

    def action_done(self):
        self.write({
            'state': 'done',
            'date_realisation': fields.Datetime.now(),
        })

    def action_cancel(self):
        self.write({'state': 'cancelled'})
