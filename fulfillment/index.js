// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';

const functions = require('firebase-functions');
const {
  WebhookClient
} = require('dialogflow-fulfillment');

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({
    request,
    response
  });
  // console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  // console.log('Dialogflow Request body: ' + JSON.stringify(request.body));

  function getBusPositionHandler(agent) {
    let http = require('http');
    const URL = 'http://qiita.com/kazuhikoyamashita/items/273692ccbdf8c0950a71.json';

    http.get(URL, (res) => {
      let body = '';
      res.setEncoding('utf8');

      res.on('data', (chunk) => {
        body += chunk;
      });

      res.on('end', (res) => {
        res = JSON.parse(body);
        console.log(res);
      });
    }).on('error', (e) => {
      console.log(e.message); //エラー時
    });
    agent.add(`This message is from Dialogflow's Cloud Functions for Firebase editor!`);
  }

  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Get SeibuBus Status', getBusPositionHandler);
  agent.handleRequest(intentMap);
});