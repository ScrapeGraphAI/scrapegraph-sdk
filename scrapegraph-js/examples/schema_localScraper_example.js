import { localScraper } from 'scrapegraph-js';
import { z } from 'zod';
import 'dotenv/config';

// localScraper function example
const apiKey = process.env.SGAI_APIKEY;
const prompt = 'extract contact';

const websiteHtml = `<html>
                      <body>
                        <h1>Company Name</h1>
                        <p>We are a technology company focused on AI solutions.</p>
                        <div class="contact">
                          <p>Email: contact@example.com</p>
                        </div>
                      </body>
                    </html>`;

const schema = z.object({
  contact: z.string().describe('email contact'),
});

try {
  const response = await localScraper(apiKey, websiteHtml, prompt, schema);
  console.log(response);
} catch (error) {
  console.error(error);
}
