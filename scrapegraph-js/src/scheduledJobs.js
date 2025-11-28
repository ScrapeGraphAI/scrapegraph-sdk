import axios from 'axios';
import handleError from './utils/handleError.js';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse } from './utils/mockResponse.js';

/**
 * Create a new scheduled job
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} jobName - Name of the scheduled job
 * @param {string} serviceType - Type of service (smartscraper, searchscraper, crawl, etc.)
 * @param {string} cronExpression - Cron expression for scheduling
 * @param {Object} jobConfig - Configuration for the job
 * @param {boolean} [isActive=true] - Whether the job is active
 * @param {Object} [options={}] - Additional options
 * @returns {Promise<Object>} Created job details
 */
export async function createScheduledJob(apiKey, jobName, serviceType, cronExpression, jobConfig, isActive = true, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for createScheduledJob');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', 'https://api.scrapegraphai.com/v1/scheduled-jobs', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/scheduled-jobs';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  const payload = {
    job_name: jobName,
    service_type: serviceType,
    cron_expression: cronExpression,
    job_config: jobConfig,
    is_active: isActive
  };

  try {
    const response = await axios.post(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Get list of scheduled jobs with pagination
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {Object} [options={}] - Query options
 * @param {number} [options.page=1] - Page number
 * @param {number} [options.pageSize=20] - Number of jobs per page
 * @param {string} [options.serviceType] - Filter by service type
 * @param {boolean} [options.isActive] - Filter by active status
 * @param {boolean} [options.mock] - Override mock mode
 * @returns {Promise<Object>} List of scheduled jobs
 */
export async function getScheduledJobs(apiKey, options = {}) {
  const { page = 1, pageSize = 20, serviceType, isActive, mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for getScheduledJobs');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('GET', 'https://api.scrapegraphai.com/v1/scheduled-jobs', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/scheduled-jobs';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  const params = { page, page_size: pageSize };
  if (serviceType) params.service_type = serviceType;
  if (isActive !== undefined) params.is_active = isActive;

  try {
    const response = await axios.get(endpoint, { headers, params });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Get details of a specific scheduled job
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} jobId - ID of the scheduled job
 * @param {Object} [options={}] - Additional options
 * @returns {Promise<Object>} Job details
 */
export async function getScheduledJob(apiKey, jobId, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for getScheduledJob');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('GET', `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}`;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  try {
    const response = await axios.get(endpoint, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Update an existing scheduled job (partial update)
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} jobId - ID of the scheduled job
 * @param {Object} updateData - Fields to update
 * @param {string} [updateData.jobName] - New job name
 * @param {string} [updateData.cronExpression] - New cron expression
 * @param {Object} [updateData.jobConfig] - New job configuration
 * @param {boolean} [updateData.isActive] - New active status
 * @param {Object} [options={}] - Additional options
 * @returns {Promise<Object>} Updated job details
 */
export async function updateScheduledJob(apiKey, jobId, updateData, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for updateScheduledJob');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('PATCH', `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}`;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  // Convert camelCase to snake_case for API
  const payload = {};
  if (updateData.jobName !== undefined) payload.job_name = updateData.jobName;
  if (updateData.cronExpression !== undefined) payload.cron_expression = updateData.cronExpression;
  if (updateData.jobConfig !== undefined) payload.job_config = updateData.jobConfig;
  if (updateData.isActive !== undefined) payload.is_active = updateData.isActive;

  try {
    const response = await axios.patch(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Replace an existing scheduled job (full update)
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} jobId - ID of the scheduled job
 * @param {string} jobName - Name of the scheduled job
 * @param {string} serviceType - Type of service
 * @param {string} cronExpression - Cron expression for scheduling
 * @param {Object} jobConfig - Configuration for the job
 * @param {boolean} [isActive=true] - Whether the job is active
 * @param {Object} [options={}] - Additional options
 * @returns {Promise<Object>} Updated job details
 */
export async function replaceScheduledJob(apiKey, jobId, jobName, serviceType, cronExpression, jobConfig, isActive = true, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for replaceScheduledJob');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('PUT', `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}`;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  const payload = {
    job_name: jobName,
    service_type: serviceType,
    cron_expression: cronExpression,
    job_config: jobConfig,
    is_active: isActive
  };

  try {
    const response = await axios.put(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Delete a scheduled job
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} jobId - ID of the scheduled job
 * @param {Object} [options={}] - Additional options
 * @returns {Promise<Object>} Deletion confirmation
 */
export async function deleteScheduledJob(apiKey, jobId, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for deleteScheduledJob');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('DELETE', `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}`;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  try {
    const response = await axios.delete(endpoint, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Pause a scheduled job
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} jobId - ID of the scheduled job
 * @param {Object} [options={}] - Additional options
 * @returns {Promise<Object>} Pause confirmation
 */
export async function pauseScheduledJob(apiKey, jobId, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for pauseScheduledJob');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}/pause`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}/pause`;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  try {
    const response = await axios.post(endpoint, {}, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Resume a paused scheduled job
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} jobId - ID of the scheduled job
 * @param {Object} [options={}] - Additional options
 * @returns {Promise<Object>} Resume confirmation
 */
export async function resumeScheduledJob(apiKey, jobId, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for resumeScheduledJob');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}/resume`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}/resume`;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  try {
    const response = await axios.post(endpoint, {}, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Manually trigger a scheduled job
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} jobId - ID of the scheduled job
 * @param {Object} [options={}] - Additional options
 * @returns {Promise<Object>} Trigger confirmation with execution ID
 */
export async function triggerScheduledJob(apiKey, jobId, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for triggerScheduledJob');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}/trigger`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}/trigger`;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  try {
    const response = await axios.post(endpoint, {}, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Get execution history for a scheduled job
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} jobId - ID of the scheduled job
 * @param {Object} [options={}] - Query options
 * @param {number} [options.page=1] - Page number
 * @param {number} [options.pageSize=20] - Number of executions per page
 * @param {string} [options.status] - Filter by execution status
 * @returns {Promise<Object>} Execution history
 */
export async function getJobExecutions(apiKey, jobId, options = {}) {
  const { page = 1, pageSize = 20, status, mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for getJobExecutions');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('GET', `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}/executions`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = `https://api.scrapegraphai.com/v1/scheduled-jobs/${jobId}/executions`;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  const params = { page, page_size: pageSize };
  if (status) params.status = status;

  try {
    const response = await axios.get(endpoint, { headers, params });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}
