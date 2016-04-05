import os

API_TOKEN = os.getenv('SLACK_TOKEN')
assert API_TOKEN, 'An SLACK_TOKEN environment variable must be set'

default_reply = "Sorry, I didn't understand you"

PLUGINS = [
    'makobot.plugins.ip',
    'makobot.plugins.url'
]

XFORCE_API_KEY = os.getenv('XFORCE_API_KEY')
XFORCE_PASSWORD = os.getenv('XFORCE_PASSWORD')
