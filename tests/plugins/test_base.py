import unittest

from makobot.plugins.base import Plugin


class PluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin= Plugin()

    def test_enabled(self):
        self.assertFalse(self.plugin.enabled)

    def test_activate(self):
        with self.assertRaises(NotImplementedError):
            self.plugin.activate()

    def test_extract(self):
        with self.assertRaises(NotImplementedError):
            self.plugin.extract(None)

    def test_report(self):
        with self.assertRaises(NotImplementedError):
            self.plugin.report(None)
