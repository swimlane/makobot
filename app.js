var builder = require('botbuilder');
var restify = require('restify');

// Create bot and add dialogs
var bot = new builder.BotConnectorBot({appId: process.env.APP_ID, appSecret: process.env.APP_SECRET});
bot.add('/', function (session) {
    session.send('Hello World');
});

// Setup Restify Server
var server = restify.createServer();
server.post('/api/messages', bot.verifyBotFramework(), bot.listen());
server.listen(process.env.PORT || 3978, function () {
    console.log('%s listening to %s', server.name, server.url); 
});