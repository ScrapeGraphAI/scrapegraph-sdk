import { localScraper, getLocalScraperRequest } from 'scrapegraph-js';
import 'dotenv/config';

// localScraper function example
const apiKey = process.env.SGAI_APIKEY;
const prompt = 'What does the company do?';

const websiteHtml = `<html>
                      <body>
                        <h1>Company Name</h1>
                        <p>We are a technology company focused on AI solutions.</p>
                        <div class="contact">
                          <p>Email: contact@example.com</p>
                        </div>
                      </body>
                    </html>`;

try {
  const response = await localScraper(apiKey, websiteHtml, prompt);
  console.log(response);
} catch (error) {
  console.error(error);
}

// getLocalScraperFunctionExample
const requestId = 'b8d97545-9ed3-441b-a01f-4b661b4f0b4c';

try {
  const response = await getLocalScraperRequest(apiKey, requestId);
  console.log(response);
} catch (error) {
  console.log(error);
}
