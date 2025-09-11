import { getMarkdownifyRequest, markdownify } from 'scrapegraph-js';
import fs from 'fs';
import 'dotenv/config';

// markdownify function example
const apiKey = process.env.SGAI_APIKEY;
const url = 'https://scrapegraphai.com/';

try {
  const response = await markdownify(apiKey, url);
  console.log(response);
  saveFile(response.result);
} catch (error) {
  console.error(error);
}

// helper function for save the file locally
function saveFile(output) {
  try {
    fs.writeFileSync('result.md', output);
    console.log('Success!');
  } catch (err) {
    console.error('Error during the file writing: ', err);
  }
}

// getMarkdownifyRequest function example
const requestId = '2563b972-cb6f-400b-be76-edb235458560';

try {
  const response = await getMarkdownifyRequest(apiKey, requestId);
  console.log(response);
} catch (error) {
  console.log(error);
}
