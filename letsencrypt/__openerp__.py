# -*- coding: utf-8 -*-
# Copyright 2016-2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
    "name": "Let's Encrypt",
    "version": "8.0.2.0.0",
    "author": "Therp BV,"
              "Tecnativa,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Hidden/Dependency",
    "summary": "Request SSL certificates from letsencrypt.org",
    "depends": [
        "base_setup",
    ],
    "data": [
        "data/ir_config_parameter.xml",
        "data/ir_cron.xml",
        "views/base_config_settings.xml",
    ],
    "demo": [
        "demo/ir_cron.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "external_dependencies": {
        "python": [
            "acme",
            "cryptography",
            "dns",
            "josepy",
        ],
    },
}
