import json
import mock
import os
import unittest

from makobot.plugins.virustotal import VirusTotalPlugin, VirusTotalIPPlugin, \
    VirusTotalMD5Plugin, VirusTotalURLPlugin

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


class VirusTotalPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = VirusTotalPlugin()

    @mock.patch('makobot.plugins.virustotal.settings', autospec=True)
    def test_enabled_false(self, mock_settings):
        mock_settings.VIRUSTOTAL_API_KEY = None
        self.assertFalse(self.plugin.enabled)

    @mock.patch('makobot.plugins.virustotal.settings', autospec=True)
    def test_enabled_true(self, mock_settings):
        mock_settings.VIRUSTOTAL_API_KEY = 'foo'
        self.assertTrue(self.plugin.enabled)

    @mock.patch('makobot.plugins.virustotal.VirusTotal', autospec=True)
    @mock.patch('makobot.plugins.virustotal.settings', autospec=True)
    def test_activatE(self, mock_settings, mock_virustotal):
        self.plugin.activate()
        mock_virustotal.assert_called_once_with(
            mock_settings.VIRUSTOTAL_API_KEY)
        self.assertEqual(self.plugin.service, mock_virustotal.return_value)

    def test_reaction(self):
        reactions = {
            0: 'sunny',
            0.02: 'mostly_sunny',
            0.04: 'partly_sunny',
            0.06: 'barely_sunny',
            0.1: 'cloud',
            0.15: 'rain_cloud',
            0.2: 'thunder_cloud_and_rain',
            0.8: 'lightning',
            0.9: 'tornado'
        }

        for score, reaction in reactions.items():
            self.assertEqual(self.plugin.reaction(score), reaction)

    def test_risk_level(self):
        risk_levels = {
            0: 'VERY LOW',
            0.02: 'LOW',
            0.1: 'MODERATE',
            0.2: 'MODERATE',
            0.4: 'HIGH',
            0.6: 'HIGH',
            0.8: 'HIGH',
            0.9: 'VERY HIGH',
            1.0: 'VERY HIGH',
            None: 'UNKNOWN'
        }

        for score, risk_level in risk_levels.items():
            self.assertEqual(self.plugin.risk_level(score), risk_level)


class VirusTotalIPPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = VirusTotalIPPlugin()

    def test_extract(self):
        self.assertTrue(hasattr(self.plugin, 'extract'))

        class Message(object):
            body = {'text': '8.8.8.8'}

        try:
            self.plugin.extract(Message())
        except NotImplementedError as e:
            self.fail(e.message)

        self.assertEqual(len(self.plugin.reports), 1)

    @mock.patch('makobot.plugins.virustotal.VirusTotal', autospec=True)
    def test_report(self, mock_virustotal):
        with open(os.path.join(DATA_DIR, 'virustotal-ip.json')) as f:
            mock_virustotal.return_value.ip.return_value = \
                json.loads(f.read())
        self.plugin.activate()
        mock_message = mock.Mock()
        mock_message.body = {'text': '123.123.123.123'}
        self.plugin.extract(mock_message)
        self.plugin.report(mock_message)
        mock_message.reply.assert_called_once_with(
            'VirusTotal IP report for 123.123.123.123 '
            'Owner: CNCGROUP IP network China169 Beijing Province Network '
            'Positives: 4504/5446 (82.7%) '
            'Risk Level: VERY HIGH')
        self.assertEqual(mock_message.mako_reaction, 'tornado')


class VirusTotalMD5(unittest.TestCase):
    def setUp(self):
        self.plugin = VirusTotalMD5Plugin()

    def test_extract(self):
        self.assertTrue(hasattr(self.plugin, 'extract'))
        mock_message = mock.Mock()
        mock_message.body = {'text': '44d88612fea8a8f36de82e1278abb02f'}
        try:
            self.plugin.extract(mock_message)
        except NotImplementedError as e:
            self.fail(e.message)
        self.assertEqual(len(self.plugin.reports), 1)

    @mock.patch('makobot.plugins.virustotal.VirusTotal', autospec=True)
    def test_report(self, mock_virustotal):
        with open(os.path.join(DATA_DIR, 'virustotal-md5.json')) as f:
            mock_virustotal.return_value.md5.return_value = \
                json.loads(f.read())
        self.plugin.activate()
        mock_message = mock.Mock()
        mock_message.body = {'text': '44d88612fea8a8f36de82e1278abb02f'}
        self.plugin.extract(mock_message)
        self.plugin.report(mock_message)
        mock_message.reply.assert_called_once_with(
            'VirusTotal Md5 report for 44d88612fea8a8f36de82e1278abb02f '
            'Positives: 55/57 (96.5%) '
            'Risk Level: VERY HIGH')
        self.assertEqual(mock_message.mako_reaction, 'tornado')


class VirusTotalURLPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = VirusTotalURLPlugin()

    def test_extract(self):
        self.assertTrue(hasattr(self.plugin, 'extract'))
        mock_message = mock.Mock()
        mock_message.body = {'text': 'http://google.com'}
        try:
            self.plugin.extract(mock_message)
        except NotImplementedError as e:
            self.fail(e.message)

    @mock.patch('makobot.plugins.virustotal.VirusTotal', autospec=True)
    def test_report(self, mock_virustotal):
        with open(os.path.join(DATA_DIR, 'virustotal-url.json')) as f:
            mock_virustotal.return_value.url.return_value = \
                json.loads(f.read())
        self.plugin.activate()
        mock_message = mock.Mock()
        mock_message.body = {'text': 'http://thepiratebay.se'}
        self.plugin.extract(mock_message)
        self.plugin.report(mock_message)
        mock_message.reply.assert_called_once_with(
            'VirusTotal URL report for http://thepiratebay.se '
            'Positives: 1/67 (1.5%) '
            'Risk Level: LOW')
        self.assertEqual(mock_message.mako_reaction, 'mostly_sunny')
