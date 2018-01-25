# -*- coding: utf-8 -*-
# Copyright - 2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class Base(models.AbstractModel):
    _inherit = 'base'
    _description = "Provide triggers on update actions."
    
    _create_before_triggers = []
    _create_after_triggers = []
    _write_before_triggers = []
    _write_after_triggers = []
    _unlink_before_triggers = []
    _unlink_after_triggers = []

    def _add_trigger(
            self, function,
            create_before=False, create_after=False,
            write_before=False, write_after=False,
            unlink_before=False, unlink_after=False,
            fields=None):
        """Add trigger to model, to fire under certain conditions.

        trigger_event can be: 'create', 'write' or 'unlink'.
        trigger_time can be: 'before', 'after'
        """
        fields = fields or []
        trigger = {'function_name': function.__name__, 'fields': fields}
        if create_before:
            self._create_before_triggers.append(trigger)
        if create_after:
            self._create_after_triggers.append(trigger)
        if write_before:
            self._write_before_triggers.append(trigger)
        if write_after:
            self._write_after_triggers.append(trigger)
        if unlink_before:
            self._unlink_before_triggers.append(trigger)
        if unlink_after:
            self._unlink_after_triggers.append(trigger)

    def _call_triggers(
            self, triggers, vals, trigger_event, trigger_time):
        """Actually call the triggers, if any."""
        ctx = self.env.context
        if not 'trigger_records' in ctx:
            ctx['trigger_records'] = {}
        elif not self._name in ctx['trigger_records']:
            ctx['trigger_records'][self._name] = {}
        else:
            id = len(self) > 0 and self.id or 0
            if id in ctx['trigger_records'][self._name]:
                return  # Prevent loop in call of triggers
            ctx['trigger_records'][self._name][id] = True
        trigger_self = self.with_context(intrigger=True)
        for trigger in triggers:
            # Check wether function only called for certain fields
            do_call = True
            if vals and trigger['fields']:
                do_call = False
                for field in trigger['fields']:
                    if field in vals:
                        do_call = True
                        break
            if do_call:
                trigger_self['function_name'](
                    vals, trigger_event, trigger_time)

    @api.model
    def create(self, vals):
        self._call_triggers(
            self._create_before_triggers, vals, 'create', 'before')
        new_rec = super(ActiveDate, self).create(vals)
        new_rec._call_triggers(
            self._create_after_triggers, vals, 'create', 'after')
        return new_rec
