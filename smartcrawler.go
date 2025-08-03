// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

package scrapegraphaisdk

import (
	"context"
	"errors"
	"fmt"
	"net/http"

	"github.com/ScrapeGraphAI/scrapegraph-sdk/internal/requestconfig"
	"github.com/ScrapeGraphAI/scrapegraph-sdk/option"
)

// SmartcrawlerService contains methods and other services that help with
// interacting with the scrapegraphai-sdk API.
//
// Note, unlike clients, this service does not read variables from the environment
// automatically. You should not instantiate this service directly, and instead use
// the [NewSmartcrawlerService] method instead.
type SmartcrawlerService struct {
	Options  []option.RequestOption
	Sessions SmartcrawlerSessionService
}

// NewSmartcrawlerService generates a new service that applies the given options to
// each request. These options are applied after the parent client's options (if
// there is one), and before any request-specific options.
func NewSmartcrawlerService(opts ...option.RequestOption) (r SmartcrawlerService) {
	r = SmartcrawlerService{}
	r.Options = opts
	r.Sessions = NewSmartcrawlerSessionService(opts...)
	return
}

// POST /smartcrawler
func (r *SmartcrawlerService) New(ctx context.Context, opts ...option.RequestOption) (err error) {
	opts = append(r.Options[:], opts...)
	opts = append([]option.RequestOption{option.WithHeader("Accept", "")}, opts...)
	path := "smartcrawler"
	err = requestconfig.ExecuteNewRequest(ctx, http.MethodPost, path, nil, nil, opts...)
	return
}

// GET /smartcrawler/{session_id}
func (r *SmartcrawlerService) Get(ctx context.Context, sessionID string, opts ...option.RequestOption) (err error) {
	opts = append(r.Options[:], opts...)
	opts = append([]option.RequestOption{option.WithHeader("Accept", "")}, opts...)
	if sessionID == "" {
		err = errors.New("missing required session_id parameter")
		return
	}
	path := fmt.Sprintf("smartcrawler/%s", sessionID)
	err = requestconfig.ExecuteNewRequest(ctx, http.MethodGet, path, nil, nil, opts...)
	return
}
