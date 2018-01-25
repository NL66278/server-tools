# -*- coding: utf-8 -*-
# Copyright - 2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class TriggerTest(models.Model):
    _name = 'trigger.test'
    _description = "Just for testing triggers"

    code = fields.Char()
    name = fields.Char()

    @api.model
    def _code_change_trigger(self, vals, trigger_event, trigger_time):
        self.write({'name': 'code=%s' % vals['code']})

    @
