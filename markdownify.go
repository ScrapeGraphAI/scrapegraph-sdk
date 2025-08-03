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

// MarkdownifyService contains methods and other services that help with
// interacting with the scrapegraphai-sdk API.
//
// Note, unlike clients, this service does not read variables from the environment
// automatically. You should not instantiate this service directly, and instead use
// the [NewMarkdownifyService] method instead.
type MarkdownifyService struct {
	Options []option.RequestOption
}

// NewMarkdownifyService generates a new service that applies the given options to
// each request. These options are applied after the parent client's options (if
// there is one), and before any request-specific options.
func NewMarkdownifyService(opts ...option.RequestOption) (r MarkdownifyService) {
	r = MarkdownifyService{}
	r.Options = opts
	return
}

// POST /markdownify
func (r *MarkdownifyService) New(ctx context.Context, opts ...option.RequestOption) (err error) {
	opts = append(r.Options[:], opts...)
	opts = append([]option.RequestOption{option.WithHeader("Accept", "")}, opts...)
	path := "v1/markdownify"
	err = requestconfig.ExecuteNewRequest(ctx, http.MethodPost, path, nil, nil, opts...)
	return
}

// GET /markdownify/{request_id}
func (r *MarkdownifyService) Get(ctx context.Context, requestID string, opts ...option.RequestOption) (err error) {
	opts = append(r.Options[:], opts...)
	opts = append([]option.RequestOption{option.WithHeader("Accept", "")}, opts...)
	if requestID == "" {
		err = errors.New("missing required request_id parameter")
		return
	}
	path := fmt.Sprintf("v1/markdownify/%s", requestID)
	err = requestconfig.ExecuteNewRequest(ctx, http.MethodGet, path, nil, nil, opts...)
	return
}
