from collections import defaultdict
import mock
import unittest

from makobot.plugins.base import Plugin
from makobot.plugins.manager import PluginManager


class PluginManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin_manager = PluginManager()

    def test_init(self):
        self.assertEqual(self.plugin_manager.plugins, defaultdict(set))

    def test_register(self):
        plugins = defaultdict(set)
        plugins['test'].add(Plugin)

        self.plugin_manager.register('test', Plugin)
        self.assertEqual(self.plugin_manager.plugins, plugins)

    def test_register_not_plugin(self):
        class Foo(object):
            pass

        with self.assertRaises(ValueError):
            self.plugin_manager.register('test', Foo)

    def test_evaluate(self):
        class MockPlugin(Plugin):
            enabled = mock.Mock()
            activate = mock.Mock()
            extract = mock.Mock()
            report = mock.Mock()
        MockPlugin.enabled.return_value = True
        mock_message = mock.Mock()
        self.plugin_manager.register('test', MockPlugin)
        self.plugin_manager.evaluate('test', mock_message)
        self.assertTrue(MockPlugin.activate.called)
        MockPlugin.extract.called_once_with(mock_message)
        MockPlugin.report.called_once_with(mock_message)
