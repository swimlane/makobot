# Makobot

Makobot will monitor your Slack channels and alert you to potential threats.
Makobot will assess the risk level of any URL, IP or file that is posted by
your Slack users and give it a weather-themed score. The sunnier the better.
When you see thunder and lightning it's probably best to avoid. If the risk
level is high enough, Makobot will provide additional details about the
potential threat.

## Installation

You can install Makobot using pip:

    pip install makobot

Makobot uses the following environment variables for configuration:

 * *SLACK_TOKEN:* Your Slack bot user token, a bot user is recommended.
 * *XFORCE_API_KEY:* If using IBM X-Force as a data source, your API key.
 * *XFORCE_PASSWORD:* Your IBM X-Force API password.

Currently only IBM X-Force is supported, but additional data sources will be
added in the future.

## Usage

Starting makobot is simple, just run:

    python -m makobot
