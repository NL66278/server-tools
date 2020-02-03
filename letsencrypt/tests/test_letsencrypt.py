# Copyright 2016 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase, tagged


class TestLetsencrypt(TransactionCase):

    @tagged('post_install', '-at_install')
    def test_letsencrypt(self):
        from ..hooks import post_init_hook
        post_init_hook(self.cr, None)
        self.env.ref('letsencrypt.config_parameter_reload').write({
            'value': '',
        })
        self.env['letsencrypt'].with_context(letsencrypt_dry_run=True).cron()
