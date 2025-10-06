import { sendFeedback } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const requestId = '16a63a80-c87f-4cde-b005-e6c3ecda278b';
const rating = 5;
const feedbackMessage = 'This is a test feedback message.';

try {
  const feedback_response = await sendFeedback(apiKey, requestId, rating, feedbackMessage);
  console.log(feedback_response);
} catch (error) {
  console.error(error);
}

const apiKey = 'your-api-key';
const requestId = 'your-request-id';
getSearchScraperRequest(apiKey, requestId)
  .then(data => console.log(data))
  .catch(error => console.error(error));
