class Plugin(object):
    @property
    def enabled(self):
        """
        REturns true if the plugin has been enabled or false if not.
        Typically this will check if the necessary environment variables are
        set.

        :returns: True if enabled, False if disabled
        :rtype: boolean
        """
        raise NotImplementedError('Plugin enabled method not implemented')

    def activate(self):
        """
        Handles the activation of the plugin, typically this would be
        instantiating a client or something similar.
        """
        raise NotImplementedError('Plugin activate method not implemented')

    def extract(self, message):
        """
        Extracts the relevant values from a message for use when generating a
        report. Values are expected to be stored as an attribute of the Plugin
        class.
        """
        raise NotImplementedError('Plugin extract method not implemented')

    def report(self, message):
        raise NotImplementedError('Plugin report method not implemented')
