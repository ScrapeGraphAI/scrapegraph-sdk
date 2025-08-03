# Credits

Methods:

- <code title="get /v1/credits">client.Credits.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#CreditService.List">List</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>

# Validate

Methods:

- <code title="get /v1/validate">client.Validate.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#ValidateService.Check">Check</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>

# Feedback

Methods:

- <code title="post /v1/feedback">client.Feedback.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#FeedbackService.New">New</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>

# Smartscraper

Methods:

- <code title="post /v1/smartscraper">client.Smartscraper.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#SmartscraperService.New">New</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>
- <code title="get /v1/smartscraper/{request_id}">client.Smartscraper.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#SmartscraperService.Get">Get</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>, requestID <a href="https://pkg.go.dev/builtin#string">string</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>

# Searchscraper

Methods:

- <code title="post /v1/searchscraper">client.Searchscraper.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#SearchscraperService.New">New</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>
- <code title="get /v1/searchscraper/{request_id}">client.Searchscraper.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#SearchscraperService.Get">Get</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>, requestID <a href="https://pkg.go.dev/builtin#string">string</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>

# Markdownify

Methods:

- <code title="post /v1/markdownify">client.Markdownify.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#MarkdownifyService.New">New</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>
- <code title="get /v1/markdownify/{request_id}">client.Markdownify.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#MarkdownifyService.Get">Get</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>, requestID <a href="https://pkg.go.dev/builtin#string">string</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>

# GenerateSchema

Methods:

- <code title="get /generate_schema/{request_id}">client.GenerateSchema.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#GenerateSchemaService.Get">Get</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>, requestID <a href="https://pkg.go.dev/builtin#string">string</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>

# Smartcrawler

Methods:

- <code title="post /smartcrawler">client.Smartcrawler.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#SmartcrawlerService.New">New</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>
- <code title="get /smartcrawler/{session_id}">client.Smartcrawler.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#SmartcrawlerService.Get">Get</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>, sessionID <a href="https://pkg.go.dev/builtin#string">string</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>

## Sessions

Methods:

- <code title="get /smartcrawler/sessions/all">client.Smartcrawler.Sessions.<a href="https://pkg.go.dev/github.com/stainless-sdks/scrapegraphai-sdk-go#SmartcrawlerSessionService.List">List</a>(ctx <a href="https://pkg.go.dev/context">context</a>.<a href="https://pkg.go.dev/context#Context">Context</a>) <a href="https://pkg.go.dev/builtin#error">error</a></code>
