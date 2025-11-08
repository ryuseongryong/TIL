// /**
//  * @type {import('@types/aws-lambda').APIGatewayProxyHandler}
//  */
// exports.handler = async (event) => {
//   console.log(`EVENT: ${JSON.stringify(event)}`);
//   return {
//     statusCode: 200,
//     //  Uncomment below to enable CORS requests
//     //  headers: {
//     //      "Access-Control-Allow-Origin": "*",
//     //      "Access-Control-Allow-Headers": "*"
//     //  },
//     body: JSON.stringify('Hello from Lambda!'),
//   };
// };
const axios = require('axios');
const moment = require('moment');

exports.handler = function (event, _, callback) {
  let apiUrl = `http://numbersapi.com/`;
  let day = moment().format('D');
  let month = moment().format('M');
  let factOfTheDay = apiUrl + month + '/' + day;

  axios
    .get(factOfTheDay)
    .then((response) => callback(null, response.data))
    .catch((err) => callback(err));
};
