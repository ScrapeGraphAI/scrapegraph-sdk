import { smartScraper, markdownify } from '../src/smartScraper.js';
import { markdownify as markdownifyFunc } from '../src/markdownify.js';

// Mock API key for testing
const MOCK_API_KEY = 'test_api_key';

// Mock axios to avoid actual HTTP calls
jest.mock('axios');

describe('Steps Functionality Tests', () => {
  let mockAxios;

  beforeEach(() => {
    mockAxios = require('axios');
    mockAxios.post.mockClear();
  });

  describe('SmartScraper with Steps', () => {
    it('should include steps in the request payload', async () => {
      const mockResponse = {
        data: {
          request_id: 'test-123',
          status: 'completed',
          result: { data: 'extracted data' }
        }
      };
      mockAxios.post.mockResolvedValue(mockResponse);

      const steps = [
        'click on search bar',
        'wait for 500ms',
        'fill search with "test"',
        'click on first result'
      ];

      const result = await smartScraper(
        MOCK_API_KEY,
        'https://example.com',
        'Extract data',
        null,
        null,
        steps
      );

      expect(mockAxios.post).toHaveBeenCalledWith(
        'https://api.scrapegraphai.com/v1/smartscraper',
        expect.objectContaining({
          website_url: 'https://example.com',
          user_prompt: 'Extract data',
          steps: steps
        }),
        expect.objectContaining({
          headers: expect.objectContaining({
            'SGAI-APIKEY': MOCK_API_KEY
          })
        })
      );

      expect(result).toEqual(mockResponse.data);
    });

    it('should work without steps parameter', async () => {
      const mockResponse = {
        data: {
          request_id: 'test-123',
          status: 'completed',
          result: { data: 'extracted data' }
        }
      };
      mockAxios.post.mockResolvedValue(mockResponse);

      const result = await smartScraper(
        MOCK_API_KEY,
        'https://example.com',
        'Extract data'
      );

      expect(mockAxios.post).toHaveBeenCalledWith(
        'https://api.scrapegraphai.com/v1/smartscraper',
        expect.objectContaining({
          website_url: 'https://example.com',
          user_prompt: 'Extract data'
        }),
        expect.objectContaining({
          headers: expect.objectContaining({
            'SGAI-APIKEY': MOCK_API_KEY
          })
        })
      );

      // Should not include steps in payload
      const calledPayload = mockAxios.post.mock.calls[0][1];
      expect(calledPayload).not.toHaveProperty('steps');
    });

    it('should throw error if steps is not an array', async () => {
      await expect(smartScraper(
        MOCK_API_KEY,
        'https://example.com',
        'Extract data',
        null,
        null,
        'invalid steps'
      )).rejects.toThrow('steps must be an array of strings');
    });

    it('should throw error if steps contains non-string values', async () => {
      await expect(smartScraper(
        MOCK_API_KEY,
        'https://example.com',
        'Extract data',
        null,
        null,
        ['valid step', 123, 'another valid step']
      )).rejects.toThrow('All steps must be strings');
    });

    it('should work with empty steps array', async () => {
      const mockResponse = {
        data: {
          request_id: 'test-123',
          status: 'completed',
          result: { data: 'extracted data' }
        }
      };
      mockAxios.post.mockResolvedValue(mockResponse);

      const result = await smartScraper(
        MOCK_API_KEY,
        'https://example.com',
        'Extract data',
        null,
        null,
        []
      );

      expect(mockAxios.post).toHaveBeenCalledWith(
        'https://api.scrapegraphai.com/v1/smartscraper',
        expect.objectContaining({
          website_url: 'https://example.com',
          user_prompt: 'Extract data',
          steps: []
        }),
        expect.objectContaining({
          headers: expect.objectContaining({
            'SGAI-APIKEY': MOCK_API_KEY
          })
        })
      );

      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('Markdownify with Steps', () => {
    it('should include steps in the request payload', async () => {
      const mockResponse = {
        data: {
          request_id: 'test-123',
          status: 'completed',
          result: '# Markdown Title\n\nContent here.'
        }
      };
      mockAxios.post.mockResolvedValue(mockResponse);

      const steps = [
        'click on accept cookies',
        'wait for 1 second',
        'scroll to main content'
      ];

      const result = await markdownifyFunc(
        MOCK_API_KEY,
        'https://example.com',
        steps
      );

      expect(mockAxios.post).toHaveBeenCalledWith(
        'https://api.scrapegraphai.com/v1/markdownify',
        expect.objectContaining({
          website_url: 'https://example.com',
          steps: steps
        }),
        expect.objectContaining({
          headers: expect.objectContaining({
            'SGAI-APIKEY': MOCK_API_KEY
          })
        })
      );

      expect(result).toEqual(mockResponse.data);
    });

    it('should work without steps parameter', async () => {
      const mockResponse = {
        data: {
          request_id: 'test-123',
          status: 'completed',
          result: '# Markdown Title\n\nContent here.'
        }
      };
      mockAxios.post.mockResolvedValue(mockResponse);

      const result = await markdownifyFunc(
        MOCK_API_KEY,
        'https://example.com'
      );

      expect(mockAxios.post).toHaveBeenCalledWith(
        'https://api.scrapegraphai.com/v1/markdownify',
        expect.objectContaining({
          website_url: 'https://example.com'
        }),
        expect.objectContaining({
          headers: expect.objectContaining({
            'SGAI-APIKEY': MOCK_API_KEY
          })
        })
      );

      // Should not include steps in payload
      const calledPayload = mockAxios.post.mock.calls[0][1];
      expect(calledPayload).not.toHaveProperty('steps');
    });

    it('should throw error if steps is not an array', async () => {
      await expect(markdownifyFunc(
        MOCK_API_KEY,
        'https://example.com',
        'invalid steps'
      )).rejects.toThrow('steps must be an array of strings');
    });

    it('should throw error if steps contains non-string values', async () => {
      await expect(markdownifyFunc(
        MOCK_API_KEY,
        'https://example.com',
        ['valid step', 123, 'another valid step']
      )).rejects.toThrow('All steps must be strings');
    });

    it('should work with empty steps array', async () => {
      const mockResponse = {
        data: {
          request_id: 'test-123',
          status: 'completed',
          result: '# Markdown Title\n\nContent here.'
        }
      };
      mockAxios.post.mockResolvedValue(mockResponse);

      const result = await markdownifyFunc(
        MOCK_API_KEY,
        'https://example.com',
        []
      );

      expect(mockAxios.post).toHaveBeenCalledWith(
        'https://api.scrapegraphai.com/v1/markdownify',
        expect.objectContaining({
          website_url: 'https://example.com',
          steps: []
        }),
        expect.objectContaining({
          headers: expect.objectContaining({
            'SGAI-APIKEY': MOCK_API_KEY
          })
        })
      );

      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('Common Step Patterns', () => {
    it('should accept authentication flow steps', async () => {
      const mockResponse = {
        data: {
          request_id: 'test-123',
          status: 'completed',
          result: { data: 'authenticated data' }
        }
      };
      mockAxios.post.mockResolvedValue(mockResponse);

      const authSteps = [
        'click on login button',
        'wait for 1 second',
        'fill username field with user@example.com',
        'wait for 200ms',
        'fill password field with password123',
        'wait for 300ms',
        'click submit button',
        'wait for 3 seconds'
      ];

      const result = await smartScraper(
        MOCK_API_KEY,
        'https://example.com/login',
        'Extract user profile after login',
        null,
        null,
        authSteps
      );

      expect(mockAxios.post).toHaveBeenCalledWith(
        'https://api.scrapegraphai.com/v1/smartscraper',
        expect.objectContaining({
          steps: authSteps
        }),
        expect.any(Object)
      );

      expect(result).toEqual(mockResponse.data);
    });

    it('should accept form interaction steps', async () => {
      const mockResponse = {
        data: {
          request_id: 'test-123',
          status: 'completed',
          result: '# Contact Form\n\nForm submitted successfully.'
        }
      };
      mockAxios.post.mockResolvedValue(mockResponse);

      const formSteps = [
        'scroll to contact form',
        'wait for 500ms',
        'fill name field with John Doe',
        'wait for 200ms',
        'fill email field with john@example.com',
        'wait for 200ms',
        'fill message field with Hello World',
        'wait for 300ms',
        'click submit button'
      ];

      const result = await markdownifyFunc(
        MOCK_API_KEY,
        'https://example.com/contact',
        formSteps
      );

      expect(mockAxios.post).toHaveBeenCalledWith(
        'https://api.scrapegraphai.com/v1/markdownify',
        expect.objectContaining({
          steps: formSteps
        }),
        expect.any(Object)
      );

      expect(result).toEqual(mockResponse.data);
    });

    it('should accept dynamic content loading steps', async () => {
      const mockResponse = {
        data: {
          request_id: 'test-123',
          status: 'completed',
          result: { data: 'loaded dynamic content' }
        }
      };
      mockAxios.post.mockResolvedValue(mockResponse);

      const dynamicSteps = [
        'scroll to bottom of page',
        'wait for 1 second',
        'click load more button',
        'wait for 2 seconds',
        'scroll down again',
        'wait for 1 second',
        'click show details button'
      ];

      const result = await smartScraper(
        MOCK_API_KEY,
        'https://example.com/dynamic',
        'Extract dynamic content',
        null,
        null,
        dynamicSteps
      );

      expect(mockAxios.post).toHaveBeenCalledWith(
        'https://api.scrapegraphai.com/v1/smartscraper',
        expect.objectContaining({
          steps: dynamicSteps
        }),
        expect.any(Object)
      );

      expect(result).toEqual(mockResponse.data);
    });
  });
}); 