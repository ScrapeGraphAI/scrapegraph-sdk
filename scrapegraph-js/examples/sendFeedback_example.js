import { sendFeedback } from 'scrapegraph-sdk';
import 'dotenv/config';

try {
  const apiKey = process.env.SGAI_APIKEY;
  const requestId = '16a63a80-c87f-4cde-b005-e6c3ecda278b';
  const rating = 5;
  const feedbackMessage = 'This is a test feedback message.';

  const feedback_response = await sendFeedback(apiKey, requestId, rating, feedbackMessage);
  console.log(feedback_response);
} catch (error) {
  console.error(error)
}