import mock
import os
import unittest

from makobot.plugins.threatconnect import ThreatConnectPlugin

#DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


class ThreatConnectPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = ThreatConnectPlugin()

    @mock.patch('makobot.plugins.threatconnect.settings', autospec=True)
    def test_enabled_false(self, mock_settings):
        mock_settings.THREATCONNECT_ACCESS_ID = None
        mock_settings.THREATCONNECT_SECRET_KEY = None
        self.assertFalse(self.plugin.enabled)

    @mock.patch('makobot.plugins.threatconnect.settings', autospec=True)
    def test_enabled_true(self, mock_settings):
        mock_settings.THREATCONNECT_ACCESS_ID = 'foo'
        mock_settings.THREATCONNECT_SECRET_KEY = 'bar'
        self.assertTrue(self.plugin.enabled)

    @mock.patch('makobot.plugins.threatconnect.ThreatConnect', autospec=True)
    @mock.patch('makobot.plugins.threatconnect.settings', autospec=True)
    def test_activatE(self, mock_settings, mock_threatconnect):
        self.plugin.activate()
        mock_threatconnect.assert_called_once_with(
            mock_settings.THREATCONNECT_ACCESS_ID,
            mock_settings.THREATCONNECT_SECRET_KEY,
            mock_settings.THREATCONNECT_DEFAULT_ORG,
            mock_settings.THREATCONNECT_BASE_URL)
        self.assertEqual(self.plugin.service, mock_threatconnect.return_value)

    def test_reaction(self):
        reactions = {
            0: 'sunny',
            0.4: 'mostly_sunny',
            0.9: 'partly_sunny',
            1.9: 'barely_sunny',
            2.4: 'cloud',
            2.9: 'rain_cloud',
            3.4: 'thunder_cloud_and_rain',
            3.9: 'lightning',
            4: 'tornado'
        }

        for score, reaction in reactions.items():
            self.assertEqual(self.plugin.reaction(score), reaction)

    def test_risk_level(self):
        risk_levels = {
            0: 'UNKNOWN',
            0.9: 'VERY LOW',
            1.9: 'LOW',
            2.9: 'MODERATE',
            3.9: 'HIGH',
            4: 'VERY HIGH',
            5: 'VERY HIGH',
            None: 'UNKNOWN'
        }

        for score, risk_level in risk_levels.items():
            self.assertEqual(self.plugin.risk_level(score), risk_level)
