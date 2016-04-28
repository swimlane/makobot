from collections import defaultdict
import inspect

from .base import Plugin


class PluginManager(object):
    def __init__(self):
        self.plugins = defaultdict(set)

    def register(self, type, plugin):
        if not inspect.isclass(plugin) or not issubclass(plugin, Plugin):
            raise ValueError(
                'Plugin must be a class and inherit from Plugin class')
        self.plugins[type].add(plugin)

    def evaluate(self, type, message):
        for plugin in self.plugins[type]:
            plugin = plugin()
            if plugin.enabled:
                plugin.activate()
                plugin.extract(message)
                plugin.report(message)


plugin_manager = PluginManager()
