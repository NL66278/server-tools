# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from cStringIO import StringIO

from odoo.exceptions import UserError
from odoo.tests import common
from odoo.tools import convert


TEST_KEY = 'ircp_from_config'
TEST_VALUE = 'config_value'


class TestEnv(common.TransactionCase):

    def setUp(self):
        super(TestEnv, self).setUp()
        self.ICP = self.env['ir.config_parameter']

    def test_get_param(self):
        """ Get system parameter from config """
        # First check tested configuration.
        self._check_expected_value(TEST_KEY, TEST_VALUE)
        # it's not in db
        res = self.ICP.search([('key', '=', TEST_KEY)])
        self.assertFalse(res)
        # read so it's created in db
        value = self.ICP.get_param(TEST_KEY)
        self.assertEqual(value, TEST_VALUE)
        # now it's in db
        res = self.ICP.search([('key', '=', TEST_KEY)])
        self.assertEqual(len(res), 1)
        self.assertEqual(res.value, TEST_VALUE)

    def test_set_param_1(self):
        """ We can't set parameters that are in config file """
        # First check tested configuration.
        self._check_expected_value(TEST_KEY, TEST_VALUE)
        # when creating, the value is overridden by config file
        self.ICP.set_param(TEST_KEY, 'new_value')
        value = self.ICP.get_param(TEST_KEY)
        self.assertEqual(value, TEST_VALUE)
        # when writing, the value is overridden by config file
        res = self.ICP.search([('key', '=', TEST_KEY)])
        self.assertEqual(len(res), 1)
        res.write({'value': 'new_value'})
        value = self.ICP.get_param(TEST_KEY)
        self.assertEqual(value, TEST_VALUE)
        # unlink works normally...
        res = self.ICP.search([('key', '=', TEST_KEY)])
        self.assertEqual(len(res), 1)
        res.unlink()
        res = self.ICP.search([('key', '=', TEST_KEY)])
        self.assertEqual(len(res), 0)
        # but the value is recreated when getting param again
        value = self.ICP.get_param(TEST_KEY)
        self.assertEqual(value, TEST_VALUE)
        res = self.ICP.search([('key', '=', TEST_KEY)])
        self.assertEqual(len(res), 1)

    def test_set_param_2(self):
        """ We can set parameters that are not in config file """
        self.ICP.set_param('some.param', 'new_value')
        self.assertEqual(self.ICP.get_param('some.param'), 'new_value')
        res = self.ICP.search([('key', '=', 'some.param')])
        res.unlink()
        res = self.ICP.search([('key', '=', 'some.param')])
        self.assertFalse(res)

    def test_empty(self):
        """ Empty config values cause error """
        # First check tested configuration.
        self._check_expected_value('ircp_empty', '')
        with self.assertRaises(UserError):
            self.ICP.get_param('ircp_empty')

    def test_not_existing(self):
        """Existing config values are equal to False."""
        self._check_expected_value('ircp_nonexistant', '# Value not set #')
        self.assertEqual(self.ICP.get_param('ircp_nonexistant'), False)

    def test_override_xmldata(self):
        # First check tested configuration.
        self._check_expected_value(TEST_KEY, TEST_VALUE)
        xml = """<odoo>
            <data>
                <record model="ir.config_parameter" id="some_record_id">
                    <field name="key">ircp_from_config</field>
                    <field name="value">value_from_xml</field>
                </record>
            </data>
        </odoo>"""
        convert.convert_xml_import(self.env.cr, 'testmodule', StringIO(xml))
        value = self.ICP.get_param(TEST_KEY)
        self.assertEqual(value, TEST_VALUE)

    def _check_expected_value(self, key, expected_value):
        """Check wether value in configuration is what test expects.

        If expected value not loaded, or loaded with wrong value,
        check the log for the files that where used to load values.
        """
        configured_value = self.ICP.peek_param(key)
        self.assertEqual(expected_value, configured_value)
