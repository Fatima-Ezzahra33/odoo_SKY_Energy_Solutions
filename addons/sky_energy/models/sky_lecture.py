# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SkyLecture(models.Model):
    _name = 'sky.lecture'
    _description = 'Lecture Énergétique'
    _order = 'date_lecture desc'

    name = fields.Char(
        string='Référence lecture',
        required=True,
        default='/',
    )
    installation_id = fields.Many2one(
        comodel_name='sky.installation',
        string='Installation',
        required=True,
        ondelete='cascade',
    )
    capteur_id = fields.Many2one(
        comodel_name='sky.capteur',
        string='Capteur',
        domain="[('installation_id', '=', installation_id)]",
    )
    date_lecture = fields.Datetime(
        string='Date de lecture',
        required=True,
        default=fields.Datetime.now,
    )
    energie_kwh = fields.Float(
        string='Énergie (kWh)',
        digits=(10, 3),
    )
    irradiation = fields.Float(
        string='Irradiation (kWh/m²)',
        digits=(10, 3),
    )
    temperature = fields.Float(
        string='Température (°C)',
        digits=(6, 2),
    )
    puissance_instantanee = fields.Float(
        string='Puissance instantanée (kW)',
        digits=(10, 3),
    )
    source = fields.Selection(
        selection=[
            ('automatique', 'Automatique'),
            ('manuel', 'Manuel'),
        ],
        string='Source',
        default='manuel',
        required=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    @api.constrains('energie_kwh')
    def _check_energie_positive(self):
        for rec in self:
            if rec.energie_kwh < 0:
                raise ValidationError("L'énergie en kWh ne peut pas être négative.")

    @api.constrains('temperature')
    def _check_temperature_realiste(self):
        for rec in self:
            if rec.temperature and not (-30 <= rec.temperature <= 90):
                raise ValidationError(
                    "La température doit être comprise entre -30°C et 90°C."
                )
