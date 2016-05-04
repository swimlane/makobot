from collections import defaultdict
import inspect
import logging

from .base import Plugin

logger = logging.getLogger(__name__)


class PluginManager(object):
    def __init__(self):
        logger.debug('Initializing plugin manager')
        self.plugins = defaultdict(set)

    def register(self, category, plugin):
        if not inspect.isclass(plugin) or not issubclass(plugin, Plugin):
            raise ValueError(
                'Plugin must be a class and inherit from Plugin class')
        logger.debug('Registering %s plugin: %s' % (category, plugin))
        self.plugins[category].add(plugin)

    def evaluate(self, category, message):
        logger.debug('Evaluating %s message: %s' % (
            category, message.body.get('text')))
        for plugin in self.plugins[category]:
            plugin = plugin()
            if plugin.enabled:
                logger.debug('Evaluating %s message with %s' % (
                    category, plugin))
                plugin.activate()
                plugin.extract(message)
                plugin.report(message)


plugin_manager = PluginManager()
