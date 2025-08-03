// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

package scrapegraphaisdk

import (
	"context"
	"errors"
	"fmt"
	"net/http"

	"github.com/stainless-sdks/scrapegraphai-sdk-go/internal/requestconfig"
	"github.com/stainless-sdks/scrapegraphai-sdk-go/option"
)

// GenerateSchemaService contains methods and other services that help with
// interacting with the scrapegraphai-sdk API.
//
// Note, unlike clients, this service does not read variables from the environment
// automatically. You should not instantiate this service directly, and instead use
// the [NewGenerateSchemaService] method instead.
type GenerateSchemaService struct {
	Options []option.RequestOption
}

// NewGenerateSchemaService generates a new service that applies the given options
// to each request. These options are applied after the parent client's options (if
// there is one), and before any request-specific options.
func NewGenerateSchemaService(opts ...option.RequestOption) (r GenerateSchemaService) {
	r = GenerateSchemaService{}
	r.Options = opts
	return
}

// GET /generate_schema/{request_id}
func (r *GenerateSchemaService) Get(ctx context.Context, requestID string, opts ...option.RequestOption) (err error) {
	opts = append(r.Options[:], opts...)
	opts = append([]option.RequestOption{option.WithHeader("Accept", "")}, opts...)
	if requestID == "" {
		err = errors.New("missing required request_id parameter")
		return
	}
	path := fmt.Sprintf("generate_schema/%s", requestID)
	err = requestconfig.ExecuteNewRequest(ctx, http.MethodGet, path, nil, nil, opts...)
	return
}
