// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

package scrapegraphaisdk_test

import (
	"context"
	"errors"
	"os"
	"testing"

	"github.com/stainless-sdks/scrapegraphai-sdk-go"
	"github.com/stainless-sdks/scrapegraphai-sdk-go/internal/testutil"
	"github.com/stainless-sdks/scrapegraphai-sdk-go/option"
)

func TestValidateCheck(t *testing.T) {
	t.Skip("skipped: tests are disabled for the time being")
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
	err := client.Validate.Check(context.TODO())
	if err != nil {
		var apierr *scrapegraphaisdk.Error
		if errors.As(err, &apierr) {
			t.Log(string(apierr.DumpRequest(true)))
		}
		t.Fatalf("err should be nil: %s", err.Error())
	}
}
