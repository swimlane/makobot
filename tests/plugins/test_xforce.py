import mock
import unittest

from makobot.plugins.xforce import XForcePlugin, XForceIPReputationPlugin, \
    XForceMD5ReputationPlugin, XForceURLReputationPlugin


class XForcePluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = XForcePlugin()

    def test_enabled(self):
        self.assertFalse(self.plugin.enabled)

    @mock.patch('makobot.plugins.xforce.settings', autospec=True)
    def test_enabled_true(self, mock_settings):
        mock_settings.XFORCE_API_KEY = 'foo'
        mock_settings.XFORCE_PASSWORD = 'bar'
        self.assertTrue(self.plugin.enabled)

    @mock.patch('makobot.plugins.xforce.XForce', autospec=True)
    def test_activatE(self, mock_xforce):
        self.plugin.activate()
        mock_xforce.assert_called_once_with(None, None)
        self.assertEqual(self.plugin.xforce, mock_xforce.return_value)

    def test_reaction(self):
        reactions = {
            1: 'sunny',
            2: 'mostly_sunny',
            3: 'partly_sunny',
            4: 'barely_sunny',
            5: 'cloud',
            6: 'rain_cloud',
            7: 'thunder_cloud_and_rain',
            8: 'lightning',
            9: 'tornado'
        }

        for score, reaction in reactions.items():
            self.assertEqual(self.plugin.reaction(score), reaction)

    def test_risk_level(self):
        risk_levels = {
            1: 'VERY LOW',
            2: 'LOW',
            3: 'MODERATE',
            4: 'MODERATE',
            5: 'HIGH',
            6: 'HIGH',
            7: 'HIGH',
            8: 'VERY HIGH',
            9: 'VERY HIGH',
            None: 'UNKNOWN'
        }

        for score, risk_level in risk_levels.items():
            self.assertEqual(self.plugin.risk_level(score), risk_level)


class XForceIPReputationPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = XForceIPReputationPlugin()

    def test_extract(self):
        self.assertTrue(hasattr(self.plugin, 'extract'))

        class Message(object):
            body = {'text': '8.8.8.8'}

        try:
            self.plugin.extract(Message())
        except NotImplementedError as e:
            self.fail(e.message)

        self.assertEqual(len(self.plugin.ips), 1)


class XForceMD5ReputationPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = XForceMD5ReputationPlugin()

    def test_extract(self):
        self.assertTrue(hasattr(self.plugin, 'extract'))

        class Message(object):
            body = {'text': '44d88612fea8a8f36de82e1278abb02f'}

        try:
            self.plugin.extract(Message())
        except NotImplementedError as e:
            self.fail(e.message)

        self.assertEqual(len(self.plugin.md5s), 1)


class XForceURLReputationPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = XForceURLReputationPlugin()

    def test_extract(self):
        self.assertTrue(hasattr(self.plugin, 'extract'))

        class Message(object):
            body = {'text': 'http://google.com'}

        try:
            self.plugin.extract(Message())
        except NotImplementedError as e:
            self.fail(e.message)

        self.assertEqual(len(self.plugin.urls), 1)
