# -*- coding: utf-8 -*-

from slackbot.bot import respond_to


@respond_to('help$')
def help(message):
    message.reply('What do you need help with?')
