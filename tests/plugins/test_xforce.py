import mock
import os
import unittest

from makobot.plugins.xforce import XForcePlugin, XForceIPPlugin, \
    XForceMD5Plugin, XForceURLPlugin


class XForcePluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = XForcePlugin()

    @mock.patch('makobot.plugins.xforce.settings', autospec=True)
    def test_enabled_false(self, mock_settings):
        mock_settings.XFORCE_API_KEY = None
        mock_settings.XFORCE_PASSWORD = None
        self.assertFalse(self.plugin.enabled)

    @mock.patch('makobot.plugins.xforce.settings', autospec=True)
    def test_enabled_true(self, mock_settings):
        mock_settings.XFORCE_API_KEY = 'foo'
        mock_settings.XFORCE_PASSWORD = 'bar'
        self.assertTrue(self.plugin.enabled)

    @mock.patch('makobot.plugins.xforce.XForce', autospec=True)
    @mock.patch('makobot.plugins.xforce.settings', autospec=True)
    def test_activatE(self, mock_settings, mock_xforce):
        self.plugin.activate()
        mock_xforce.assert_called_once_with(
            mock_settings.XFORCE_API_KEY,
            mock_settings.XFORCE_PASSWORD
        )
        self.assertEqual(self.plugin.service, mock_xforce.return_value)

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


class XForceIPPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = XForceIPPlugin()

    def test_extract(self):
        self.assertTrue(hasattr(self.plugin, 'extract'))

        class Message(object):
            body = {'text': '8.8.8.8'}

        try:
            self.plugin.extract(Message())
        except NotImplementedError as e:
            self.fail(e.message)

        self.assertEqual(len(self.plugin.reports), 1)

    def test_report(self):
        api_key = os.getenv('XFORCE_API_KEY')
        api_password = os.getenv('XFORCE_PASSWORD')
        if not api_key or not api_password:
            raise unittest.SkipTest(
                'XFORCE_API_KEY and XFORCE_API_PASSWORD environment '
                'variables must be set to run this test')

        self.plugin.activate()

        mock_message = mock.Mock()
        mock_message.body = {'text': '123.123.123.123'}
        self.plugin.extract(mock_message)
        self.plugin.report(mock_message)
        mock_message.reply.assert_called_once_with(
            'X-Force IP report for 123.123.123.123 '
            'Score: 1 Risk Level: VERY LOW Reason: Community feedback')
        self.assertEqual(mock_message.mako_reaction, 'sunny')


class XForceMD5(unittest.TestCase):
    def setUp(self):
        self.plugin = XForceMD5Plugin()

    def test_extract(self):
        self.assertTrue(hasattr(self.plugin, 'extract'))

        class Message(object):
            body = {'text': '44d88612fea8a8f36de82e1278abb02f'}

        try:
            self.plugin.extract(Message())
        except NotImplementedError as e:
            self.fail(e.message)

        self.assertEqual(len(self.plugin.reports), 1)

    def test_report(self):
        api_key = os.getenv('XFORCE_API_KEY')
        api_password = os.getenv('XFORCE_PASSWORD')
        if not api_key or not api_password:
            raise unittest.SkipTest(
                'XFORCE_API_KEY and XFORCE_API_PASSWORD environment '
                'variables must be set to run this test')

        self.plugin.activate()
        mock_message = mock.Mock()
        mock_message.body = {'text': '44d88612fea8a8f36de82e1278abb02f'}
        self.plugin.extract(mock_message)
        self.plugin.report(mock_message)
        self.assertEqual(mock_message.mako_reaction, 'lightning')


class XForceURLPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = XForceURLPlugin()

    def test_extract(self):
        self.assertTrue(hasattr(self.plugin, 'extract'))

        class Message(object):
            body = {'text': 'http://google.com'}

        try:
            self.plugin.extract(Message())
        except NotImplementedError as e:
            self.fail(e.message)

    def test_report(self):
        api_key = os.getenv('XFORCE_API_KEY')
        api_password = os.getenv('XFORCE_PASSWORD')
        if not api_key or not api_password:
            raise unittest.SkipTest(
                'XFORCE_API_KEY and XFORCE_API_PASSWORD environment '
                'variables must be set to run this test')

        self.plugin.activate()
        mock_message = mock.Mock()
        mock_message.body = {'text': 'https://www.thepiratebay.se'}
        self.plugin.extract(mock_message)
        self.plugin.report(mock_message)
        mock_message.reply.assert_called_once_with(
            'X-Force URL report for https://www.thepiratebay.se '
            'Score: 10 Risk Level: VERY HIGH '
            'Categories: Warez / Software Piracy, Illegal Activities, '
            'Search Engines / Web Catalogues / Portals, '
            'Computer Crime / Hacking')
        self.assertEqual(mock_message.mako_reaction, 'tornado')
