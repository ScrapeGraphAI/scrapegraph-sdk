# 🤖 Agentic Scraper

The Agentic Scraper enables AI-powered browser automation for complex interactions like form filling, clicking buttons, and navigating multi-step workflows.

## 🚀 Quick Start

### Basic Usage (No AI Extraction)
```javascript
import { agenticScraper, getAgenticScraperRequest } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const url = 'https://dashboard.scrapegraphai.com/';
const steps = [
  'Type email@gmail.com in email input box',
  'Type test-password@123 in password inputbox',
  'click on login'
];

// Submit automation request (basic scraping)
const response = await agenticScraper(apiKey, url, steps, true);
console.log('Request ID:', response.request_id);

// Check results
const result = await getAgenticScraperRequest(apiKey, response.request_id);
console.log('Status:', result.status);
console.log('Markdown Content:', result.markdown);
```

### AI Extraction Usage
```javascript
import { agenticScraper, getAgenticScraperRequest } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const url = 'https://dashboard.scrapegraphai.com/';
const steps = [
  'Type email@gmail.com in email input box',
  'Type test-password@123 in password inputbox',
  'click on login',
  'wait for dashboard to load'
];

// Define extraction schema
const outputSchema = {
  user_info: {
    type: "object",
    properties: {
      username: { type: "string" },
      email: { type: "string" },
      dashboard_sections: { type: "array", items: { type: "string" } }
    }
  }
};

// Submit automation request with AI extraction
const response = await agenticScraper(
  apiKey, 
  url, 
  steps, 
  true,                                                    // useSession
  "Extract user information and available dashboard sections", // userPrompt
  outputSchema,                                            // outputSchema
  true                                                     // aiExtraction
);

console.log('Request ID:', response.request_id);

// Check results
const result = await getAgenticScraperRequest(apiKey, response.request_id);
if (result.status === 'completed') {
  console.log('Extracted Data:', result.result);
  console.log('Raw Markdown:', result.markdown);
}
```

## 📚 API Reference

### `agenticScraper(apiKey, url, steps, useSession, userPrompt, outputSchema, aiExtraction)`

Performs automated browser actions on a webpage with optional AI extraction.

**Parameters:**
- `apiKey` (string): Your ScrapeGraph AI API key
- `url` (string): The URL of the webpage to interact with
- `steps` (string[]): Array of automation steps to perform
- `useSession` (boolean, optional): Whether to use session management (default: true)
- `userPrompt` (string, optional): Prompt for AI extraction (required when aiExtraction=true)
- `outputSchema` (object, optional): Schema for structured data extraction (used with aiExtraction=true)
- `aiExtraction` (boolean, optional): Whether to use AI for data extraction (default: false)

**Returns:** Promise<Object> with `request_id` and initial `status`

**Example Steps:**
```javascript
const steps = [
  'click on search bar',
  'type "laptop" in search input',
  'press Enter key',
  'wait for 2 seconds',
  'click on first result',
  'scroll down to reviews'
];
```

### `getAgenticScraperRequest(apiKey, requestId)`

Retrieves the status or result of an agentic scraper request.

**Parameters:**
- `apiKey` (string): Your ScrapeGraph AI API key  
- `requestId` (string): The request ID from a previous agentic scraper call

**Returns:** Promise<Object> with:
- `status`: 'pending', 'completed', or 'failed'
- `result`: Automation results (when completed)
- `error`: Error message (when failed)
- `created_at`: Request creation timestamp
- `completed_at`: Completion timestamp (when completed)

## 🎯 Use Cases

### 1. **Basic Automation (No AI)**
Perfect for simple automation tasks where you just need the raw HTML/markdown content:
- **Login automation**: Automate login flows and capture the resulting page
- **Form submission**: Fill out forms and get confirmation pages
- **Navigation**: Navigate through multi-step workflows
- **Content scraping**: Get page content after performing actions

### 2. **AI-Powered Data Extraction**
Ideal when you need structured data from the automated interactions:
- **Dashboard data extraction**: Login and extract user information, metrics, settings
- **E-commerce scraping**: Search products and extract structured product data
- **Form result parsing**: Submit forms and extract confirmation details, reference numbers
- **Content analysis**: Navigate to content and extract key information in structured format

### 3. **Hybrid Approach**
Use both modes depending on your needs:
- **Development/Testing**: Start with basic mode to test automation steps
- **Production**: Add AI extraction for structured data processing
- **Fallback**: Use basic mode when AI extraction isn't needed

## 💡 AI Extraction Examples

### E-commerce Product Search
```javascript
const steps = [
  'click on search box',
  'type "wireless headphones" in search',
  'press enter',
  'wait for results to load',
  'scroll down 2 times'
];

const schema = {
  products: {
    type: "array",
    items: {
      type: "object", 
      properties: {
        name: { type: "string" },
        price: { type: "string" },
        rating: { type: "number" },
        availability: { type: "string" }
      }
    }
  }
};

const response = await agenticScraper(
  apiKey, 
  'https://example-store.com', 
  steps, 
  true,
  'Extract product names, prices, ratings, and availability from search results',
  schema,
  true
);
```

### Contact Form with Confirmation
```javascript
const steps = [
  'type "John Doe" in name field',
  'type "john@example.com" in email field',
  'type "Product inquiry" in subject field',
  'type "I need more information about pricing" in message field',
  'click submit button',
  'wait for confirmation'
];

const schema = {
  submission: {
    type: "object",
    properties: {
      status: { type: "string" },
      message: { type: "string" },
      reference_number: { type: "string" },
      response_time: { type: "string" }
    }
  }
};

const response = await agenticScraper(
  apiKey,
  'https://company.com/contact',
  steps,
  true,
  'Extract form submission status, confirmation message, and any reference numbers',
  schema,
  true
);
```

### Social Media Data Extraction
```javascript
const steps = [
  'type "username" in username field',
  'type "password" in password field', 
  'click login button',
  'wait for dashboard',
  'click on profile section'
];

const schema = {
  profile: {
    type: "object",
    properties: {
      username: { type: "string" },
      followers: { type: "number" },
      following: { type: "number" },
      posts: { type: "number" },
      recent_activity: { type: "array", items: { type: "string" } }
    }
  }
};

const response = await agenticScraper(
  apiKey,
  'https://social-platform.com/login',
  steps,
  true,
  'Extract profile information including username, follower counts, and recent activity',
  schema,
  true
);
```

## 🔧 Best Practices

### When to Use AI Extraction
- ✅ **Use AI extraction when**: You need structured data, specific information extraction, or data validation
- ❌ **Skip AI extraction when**: You just need raw content, testing automation steps, or processing content externally

### Schema Design Tips
- **Be specific**: Define exact data types and required fields
- **Use descriptions**: Add description fields to guide AI extraction
- **Nested objects**: Use nested schemas for complex data structures
- **Arrays**: Use arrays for lists of similar items (products, comments, etc.)

### Step Optimization
- **Wait steps**: Add wait steps after actions that trigger loading
- **Specific selectors**: Use specific element descriptions ("click on blue submit button")
- **Sequential actions**: Break complex actions into smaller, specific steps
- **Error handling**: Include steps to handle common UI variations

### 🔐 Login Automation
```javascript
const loginSteps = [
  'click on email input',
  'type "user@example.com" in email field',
  'click on password input',
  'type "password123" in password field',
  'click login button',
  'wait for dashboard to load'
];

const response = await agenticScraper(apiKey, 'https://app.example.com/login', loginSteps, true);
```

### 🛒 E-commerce Interaction
```javascript
const shoppingSteps = [
  'click on search bar',
  'type "wireless headphones" in search',
  'press Enter',
  'wait for results to load',
  'click on first product',
  'click add to cart button',
  'click view cart'
];

const response = await agenticScraper(apiKey, 'https://shop.example.com', shoppingSteps, true);
```

### 📝 Form Submission
```javascript
const formSteps = [
  'click on name input',
  'type "John Doe" in name field',
  'click on email input', 
  'type "john@example.com" in email field',
  'click on message textarea',
  'type "Hello, this is a test message" in message area',
  'click submit button'
];

const response = await agenticScraper(apiKey, 'https://example.com/contact', formSteps, false);
```

## ⚡ Advanced Usage

### Polling for Results
```javascript
async function waitForCompletion(requestId, timeoutSeconds = 120) {
  const startTime = Date.now();
  const timeout = timeoutSeconds * 1000;
  
  while (Date.now() - startTime < timeout) {
    const status = await getAgenticScraperRequest(apiKey, requestId);
    
    if (status.status === 'completed') {
      return status.result;
    } else if (status.status === 'failed') {
      throw new Error(status.error);
    }
    
    await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds
  }
  
  throw new Error('Timeout waiting for completion');
}
```

### Error Handling
```javascript
try {
  const response = await agenticScraper(apiKey, url, steps, true);
  const result = await waitForCompletion(response.request_id);
  console.log('Automation successful:', result);
} catch (error) {
  if (error.message.includes('validation')) {
    console.log('Input validation failed:', error.message);
  } else if (error.message.includes('timeout')) {
    console.log('Automation timed out');
  } else {
    console.log('Automation failed:', error.message);
  }
}
```

## 📝 Step Syntax

Steps should be written in natural language describing the action to perform:

### Clicking Elements
- `"click on login button"`
- `"click on search icon"`
- `"click on first result"`

### Typing Text
- `"type 'username' in email field"`
- `"type 'password123' in password input"`
- `"type 'search query' in search box"`

### Keyboard Actions
- `"press Enter key"`
- `"press Tab key"`
- `"press Escape key"`

### Waiting
- `"wait for 2 seconds"`
- `"wait for page to load"`
- `"wait for results to appear"`

### Scrolling
- `"scroll down"`
- `"scroll to bottom"`
- `"scroll to top"`

## 🔧 Best Practices

1. **Use Session Management**: Set `useSession: true` for multi-step workflows
2. **Add Wait Steps**: Include wait times between actions for reliability
3. **Be Specific**: Use descriptive selectors like "login button" vs "button"
4. **Handle Timeouts**: Implement proper timeout handling for long operations
5. **Validate Inputs**: Check URLs and steps before making requests

## 🚨 Common Errors

### Input Validation Errors
```javascript
// ❌ Invalid URL
await agenticScraper(apiKey, 'not-a-url', steps); 

// ❌ Empty steps
await agenticScraper(apiKey, url, []);

// ❌ Invalid step
await agenticScraper(apiKey, url, ['click button', '']); // Empty step
```

### Runtime Errors
- **Element not found**: Make steps more specific or add wait times
- **Timeout**: Increase polling timeout or break down complex steps
- **Session expired**: Use session management for multi-step flows

## 🌐 cURL Equivalent

```bash
curl --location 'https://api.scrapegraphai.com/v1/agentic-scrapper' \
--header 'SGAI-APIKEY: your-api-key' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "https://dashboard.scrapegraphai.com/",
    "use_session": true,
    "steps": [
        "Type email@gmail.com in email input box",
        "Type test-password@123 in password inputbox", 
        "click on login"
    ]
}'
```

## 📖 Examples

Check out the example files in the `/examples` directory:

- `agenticScraper_example.js` - Basic usage
- `getAgenticScraperRequest_example.js` - Status checking  
- `agenticScraper_complete_example.js` - Complete workflow
- `agenticScraper_advanced_example.js` - Advanced patterns with error handling

## 💡 Tips

- Start with simple steps and gradually add complexity
- Test individual steps before combining them
- Use browser developer tools to identify element selectors
- Consider mobile vs desktop layouts when writing steps
- Monitor request status regularly for long-running automations
