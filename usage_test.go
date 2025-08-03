// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

package scrapegraphaisdk_test

import (
	"context"
	"os"
	"testing"

	"github.com/ScrapeGraphAI/scrapegraph-sdk"
	"github.com/ScrapeGraphAI/scrapegraph-sdk/internal/testutil"
	"github.com/ScrapeGraphAI/scrapegraph-sdk/option"
)

func TestUsage(t *testing.T) {
	baseURL := "http://localhost:4010"
	if envURL, ok := os.LookupEnv("TEST_API_BASE_URL"); ok {
		baseURL = envURL
	}
	if !testutil.CheckTestServer(t, baseURL) {
		return
	}
	client := scrapegraphaisdk.NewClient(
		option.WithBaseURL(baseURL),
		option.WithAPIKey("My API Key"),
	)
	err := client.Credits.List(context.TODO())
	if err != nil {
		t.Fatalf("err should be nil: %s", err.Error())
	}
}
