// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

package scrapegraphaisdk

import (
	"context"
	"net/http"

	"github.com/ScrapeGraphAI/scrapegraph-sdk/internal/requestconfig"
	"github.com/ScrapeGraphAI/scrapegraph-sdk/option"
)

// CreditService contains methods and other services that help with interacting
// with the scrapegraphai-sdk API.
//
// Note, unlike clients, this service does not read variables from the environment
// automatically. You should not instantiate this service directly, and instead use
// the [NewCreditService] method instead.
type CreditService struct {
	Options []option.RequestOption
}

// NewCreditService generates a new service that applies the given options to each
// request. These options are applied after the parent client's options (if there
// is one), and before any request-specific options.
func NewCreditService(opts ...option.RequestOption) (r CreditService) {
	r = CreditService{}
	r.Options = opts
	return
}

// GET /credits
func (r *CreditService) List(ctx context.Context, opts ...option.RequestOption) (err error) {
	opts = append(r.Options[:], opts...)
	opts = append([]option.RequestOption{option.WithHeader("Accept", "")}, opts...)
	path := "v1/credits"
	err = requestconfig.ExecuteNewRequest(ctx, http.MethodGet, path, nil, nil, opts...)
	return
}
