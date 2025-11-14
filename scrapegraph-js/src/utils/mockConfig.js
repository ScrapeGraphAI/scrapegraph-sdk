/**
 * Mock configuration utility for ScrapeGraph AI SDK
 * Manages global mock settings and configuration
 */

// Global mock configuration
let mockConfig = {
  enabled: false,
  customResponses: {},
  customHandler: null
};

/**
 * Check if mock mode is enabled via environment variable
 * @returns {boolean} True if mock mode should be enabled
 */
function isMockEnabledFromEnv() {
  if (typeof process !== 'undefined' && process.env) {
    const mockEnv = process.env.SGAI_MOCK;
    if (mockEnv) {
      return ['1', 'true', 'True', 'TRUE', 'yes', 'YES', 'on', 'ON'].includes(mockEnv.trim());
    }
  }
  return false;
}

/**
 * Initialize mock configuration
 * @param {Object} options - Mock configuration options
 * @param {boolean} options.enabled - Whether mock mode is enabled
 * @param {Object} options.customResponses - Custom response overrides
 * @param {Function} options.customHandler - Custom handler function
 */
export function initMockConfig(options = {}) {
  const {
    enabled = isMockEnabledFromEnv(),
    customResponses = {},
    customHandler = null
  } = options;

  mockConfig = {
    enabled: Boolean(enabled),
    customResponses: { ...customResponses },
    customHandler: customHandler
  };

  if (mockConfig.enabled) {
    console.log('🧪 ScrapeGraph AI SDK: Mock mode enabled');
  }
}

/**
 * Get current mock configuration
 * @returns {Object} Current mock configuration
 */
export function getMockConfig() {
  return { ...mockConfig };
}

/**
 * Check if mock mode is currently enabled
 * @returns {boolean} True if mock mode is enabled
 */
export function isMockEnabled() {
  return mockConfig.enabled;
}

/**
 * Set custom responses for specific endpoints
 * @param {Object} responses - Map of endpoint paths to responses
 */
export function setMockResponses(responses) {
  mockConfig.customResponses = { ...mockConfig.customResponses, ...responses };
}

/**
 * Set a custom mock handler function
 * @param {Function} handler - Custom handler function
 */
export function setMockHandler(handler) {
  mockConfig.customHandler = handler;
}

/**
 * Disable mock mode
 */
export function disableMock() {
  mockConfig.enabled = false;
}

/**
 * Enable mock mode
 */
export function enableMock() {
  mockConfig.enabled = true;
  console.log('🧪 ScrapeGraph AI SDK: Mock mode enabled');
}

// Initialize with environment check
initMockConfig();
