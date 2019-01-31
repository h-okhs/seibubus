// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';

const functions = require('firebase-functions');
const {
  WebhookClient
} = require('dialogflow-fulfillment');
const {
  Card,
  Suggestion
} = require('dialogflow-fulfillment');

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({
    request,
    response
  });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));

  function getBusPositionHandler(agent) {
    let http = require('https');
    const URL = 'https://lighteater.com/ws/index.cgi/busapi/v1/busstatuses';

    http.get(URL, (res) => {
      let body = '';
      res.setEncoding('utf8');

      res.on('data', (chunk) => {
        body += chunk;
      });

      res.on('end', (res) => {
        res = JSON.parse(body);

        let message = '';
        res.busstatuses.forEach(element => {
          message += element.line + ' ' + element.departureAt + ' ';
        });
        agent.add(message);
      });
    }).on('error', (e) => {
      console.log(e.message); //エラー時
    });
  }

  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Get SeibuBus Status', getBusPositionHandler);
  agent.handleRequest(intentMap);
});