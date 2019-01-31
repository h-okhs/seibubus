// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';

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
    console.log(res);

    let busstatusArray = res.busstatuses;
    let message = '';
    busstatusArray.forEach(element => {
      message += element.line + ' ' + element.departureAt + ':';
    });
    console.log(message);
  });
}).on('error', (e) => {
  console.log(e.message); //エラー時
});