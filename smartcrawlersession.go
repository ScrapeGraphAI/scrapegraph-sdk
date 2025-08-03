// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

package scrapegraphaisdk

import (
	"context"
	"net/http"

	"github.com/stainless-sdks/scrapegraphai-sdk-go/internal/requestconfig"
	"github.com/stainless-sdks/scrapegraphai-sdk-go/option"
)

// SmartcrawlerSessionService contains methods and other services that help with
// interacting with the scrapegraphai-sdk API.
//
// Note, unlike clients, this service does not read variables from the environment
// automatically. You should not instantiate this service directly, and instead use
// the [NewSmartcrawlerSessionService] method instead.
type SmartcrawlerSessionService struct {
	Options []option.RequestOption
}

// NewSmartcrawlerSessionService generates a new service that applies the given
// options to each request. These options are applied after the parent client's
// options (if there is one), and before any request-specific options.
func NewSmartcrawlerSessionService(opts ...option.RequestOption) (r SmartcrawlerSessionService) {
	r = SmartcrawlerSessionService{}
	r.Options = opts
	return
}

// GET /smartcrawler/sessions/all
func (r *SmartcrawlerSessionService) List(ctx context.Context, opts ...option.RequestOption) (err error) {
	opts = append(r.Options[:], opts...)
	opts = append([]option.RequestOption{option.WithHeader("Accept", "")}, opts...)
	path := "smartcrawler/sessions/all"
	err = requestconfig.ExecuteNewRequest(ctx, http.MethodGet, path, nil, nil, opts...)
	return
}
