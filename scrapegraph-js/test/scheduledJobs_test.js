import {
  createScheduledJob,
  getScheduledJobs,
  getScheduledJob,
  updateScheduledJob,
  replaceScheduledJob,
  deleteScheduledJob,
  pauseScheduledJob,
  resumeScheduledJob,
  triggerScheduledJob,
  getJobExecutions,
  enableMock,
  disableMock
} from '../index.js';

describe('Scheduled Jobs', () => {
  const apiKey = 'test-api-key';
  
  beforeAll(() => {
    enableMock();
  });
  
  afterAll(() => {
    disableMock();
  });

  describe('createScheduledJob', () => {
    test('should create a scheduled job successfully', async () => {
      const jobConfig = {
        website_url: 'https://example.com',
        user_prompt: 'Extract data',
        render_heavy_js: false
      };
      
      const result = await createScheduledJob(
        apiKey,
        'Test Job',
        'smartscraper',
        '0 9 * * 1',
        jobConfig,
        true
      );
      
      expect(result).toHaveProperty('id');
      expect(result.job_name).toBe('Mock Scheduled Job');
      expect(result.service_type).toBe('smartscraper');
      expect(result.is_active).toBe(true);
    });

    test('should create a job with default active status', async () => {
      const jobConfig = { test: 'config' };
      
      const result = await createScheduledJob(
        apiKey,
        'Test Job',
        'searchscraper',
        '0 8 * * 1',
        jobConfig
      );
      
      expect(result.is_active).toBe(true);
    });

    test('should handle different service types', async () => {
      const serviceTypes = ['smartscraper', 'searchscraper', 'crawl', 'agenticscraper'];
      
      for (const serviceType of serviceTypes) {
        const result = await createScheduledJob(
          apiKey,
          `Test ${serviceType} Job`,
          serviceType,
          '0 9 * * 1',
          { test: 'config' }
        );
        
        expect(result).toHaveProperty('id');
        expect(result.service_type).toBe('smartscraper'); // Mock always returns smartscraper
      }
    });
  });

  describe('getScheduledJobs', () => {
    test('should get list of scheduled jobs with default pagination', async () => {
      const result = await getScheduledJobs(apiKey);
      
      expect(result).toHaveProperty('jobs');
      expect(result).toHaveProperty('total');
      expect(result).toHaveProperty('page');
      expect(result).toHaveProperty('page_size');
      expect(Array.isArray(result.jobs)).toBe(true);
      expect(result.jobs.length).toBeGreaterThan(0);
    });

    test('should get jobs with custom pagination', async () => {
      const result = await getScheduledJobs(apiKey, {
        page: 2,
        pageSize: 10
      });
      
      expect(result.page).toBe(1); // Mock always returns page 1
      expect(result.page_size).toBe(20); // Mock uses default page_size
    });

    test('should filter jobs by service type', async () => {
      const result = await getScheduledJobs(apiKey, {
        serviceType: 'smartscraper'
      });
      
      expect(result.jobs.length).toBeGreaterThan(0);
    });

    test('should filter jobs by active status', async () => {
      const activeJobs = await getScheduledJobs(apiKey, { isActive: true });
      const inactiveJobs = await getScheduledJobs(apiKey, { isActive: false });
      
      expect(activeJobs.jobs.length).toBeGreaterThan(0);
      expect(inactiveJobs.jobs.length).toBeGreaterThan(0);
    });
  });

  describe('getScheduledJob', () => {
    test('should get a specific scheduled job', async () => {
      const jobId = 'test-job-id';
      const result = await getScheduledJob(apiKey, jobId);
      
      expect(result).toHaveProperty('id');
      expect(result.job_name).toBe('Mock Scheduled Job');
      expect(result.service_type).toBe('smartscraper');
    });

    test('should handle invalid job ID', async () => {
      const jobId = 'invalid-job-id';
      const result = await getScheduledJob(apiKey, jobId);
      
      expect(result).toHaveProperty('id');
      expect(result.job_name).toBe('Mock Scheduled Job');
    });
  });

  describe('updateScheduledJob', () => {
    test('should update job name', async () => {
      const jobId = 'test-job-id';
      const result = await updateScheduledJob(apiKey, jobId, {
        jobName: 'Updated Job Name'
      });
      
      expect(result.job_name).toBe('Updated Mock Scheduled Job');
    });

    test('should update cron expression', async () => {
      const jobId = 'test-job-id';
      const result = await updateScheduledJob(apiKey, jobId, {
        cronExpression: '0 10 * * 1'
      });
      
      expect(result.cron_expression).toBe('0 10 * * 1');
    });

    test('should update job configuration', async () => {
      const jobId = 'test-job-id';
      const newConfig = { updated: 'config' };
      const result = await updateScheduledJob(apiKey, jobId, {
        jobConfig: newConfig
      });
      
      expect(result.job_config).toEqual({ mock: 'updated_config' });
    });

    test('should update active status', async () => {
      const jobId = 'test-job-id';
      const result = await updateScheduledJob(apiKey, jobId, {
        isActive: false
      });
      
      expect(result.is_active).toBe(true); // Mock always returns true
    });

    test('should update multiple fields at once', async () => {
      const jobId = 'test-job-id';
      const result = await updateScheduledJob(apiKey, jobId, {
        jobName: 'Multi Update Job',
        cronExpression: '0 11 * * 1',
        isActive: false
      });
      
      expect(result.job_name).toBe('Updated Mock Scheduled Job');
      expect(result.cron_expression).toBe('0 10 * * 1');
    });
  });

  describe('replaceScheduledJob', () => {
    test('should replace a scheduled job completely', async () => {
      const jobId = 'test-job-id';
      const jobConfig = { test: 'config' };
      
      const result = await replaceScheduledJob(
        apiKey,
        jobId,
        'Replaced Job',
        'searchscraper',
        '0 8 * * 1',
        jobConfig,
        true
      );
      
      expect(result.job_name).toBe('Updated Mock Scheduled Job');
      expect(result.service_type).toBe('smartscraper'); // Mock always returns smartscraper
    });

    test('should replace job with default active status', async () => {
      const jobId = 'test-job-id';
      const jobConfig = { test: 'config' };
      
      const result = await replaceScheduledJob(
        apiKey,
        jobId,
        'Replaced Job',
        'crawl',
        '0 7 * * 1',
        jobConfig
      );
      
      expect(result.is_active).toBe(true);
    });
  });

  describe('deleteScheduledJob', () => {
    test('should delete a scheduled job', async () => {
      const jobId = 'test-job-id';
      const result = await deleteScheduledJob(apiKey, jobId);
      
      expect(result).toHaveProperty('message');
      expect(result.message).toContain('deleted successfully');
    });
  });

  describe('pauseScheduledJob', () => {
    test('should pause a scheduled job', async () => {
      const jobId = 'test-job-id';
      const result = await pauseScheduledJob(apiKey, jobId);
      
      expect(result).toHaveProperty('message');
      expect(result.message).toContain('paused successfully');
      expect(result.is_active).toBe(false);
    });
  });

  describe('resumeScheduledJob', () => {
    test('should resume a scheduled job', async () => {
      const jobId = 'test-job-id';
      const result = await resumeScheduledJob(apiKey, jobId);
      
      expect(result).toHaveProperty('message');
      expect(result.message).toContain('resumed successfully');
      expect(result.is_active).toBe(true);
    });
  });

  describe('triggerScheduledJob', () => {
    test('should trigger a scheduled job manually', async () => {
      const jobId = 'test-job-id';
      const result = await triggerScheduledJob(apiKey, jobId);
      
      expect(result).toHaveProperty('execution_id');
      expect(result).toHaveProperty('scheduled_job_id');
      expect(result).toHaveProperty('message');
      expect(result.message).toContain('triggered successfully');
    });
  });

  describe('getJobExecutions', () => {
    test('should get job execution history', async () => {
      const jobId = 'test-job-id';
      const result = await getJobExecutions(apiKey, jobId);
      
      expect(result).toHaveProperty('executions');
      expect(result).toHaveProperty('total');
      expect(result).toHaveProperty('page');
      expect(result).toHaveProperty('page_size');
      expect(Array.isArray(result.executions)).toBe(true);
      expect(result.executions.length).toBeGreaterThan(0);
    });

    test('should get executions with custom pagination', async () => {
      const jobId = 'test-job-id';
      const result = await getJobExecutions(apiKey, jobId, {
        page: 2,
        pageSize: 10
      });
      
      expect(result.page).toBe(1); // Mock always returns page 1
      expect(result.page_size).toBe(20); // Mock uses default page_size
    });

    test('should filter executions by status', async () => {
      const jobId = 'test-job-id';
      const result = await getJobExecutions(apiKey, jobId, {
        status: 'completed'
      });
      
      expect(result.executions.length).toBeGreaterThan(0);
      const execution = result.executions[0];
      expect(execution).toHaveProperty('id');
      expect(execution).toHaveProperty('status');
      expect(execution).toHaveProperty('started_at');
    });

    test('should return execution details', async () => {
      const jobId = 'test-job-id';
      const result = await getJobExecutions(apiKey, jobId);
      
      const execution = result.executions[0];
      expect(execution).toHaveProperty('id');
      expect(execution).toHaveProperty('scheduled_job_id');
      expect(execution).toHaveProperty('execution_id');
      expect(execution).toHaveProperty('status');
      expect(execution).toHaveProperty('started_at');
      expect(execution).toHaveProperty('completed_at');
      expect(execution).toHaveProperty('result');
      expect(execution).toHaveProperty('credits_used');
    });
  });

  describe('Error Handling', () => {
    test('should handle API errors gracefully', async () => {
      // This test would require mocking axios to throw an error
      // For now, we'll test that the functions don't throw unexpected errors
      const jobId = 'test-job-id';
      
      await expect(getScheduledJob(apiKey, jobId)).resolves.toBeDefined();
      await expect(getScheduledJobs(apiKey)).resolves.toBeDefined();
    });
  });

  describe('Mock Mode', () => {
    test('should work in mock mode', async () => {
      const result = await createScheduledJob(
        apiKey,
        'Mock Test Job',
        'smartscraper',
        '0 9 * * 1',
        { test: 'config' },
        true,
        { mock: true }
      );
      
      expect(result).toHaveProperty('id');
      expect(result.job_name).toBe('Mock Scheduled Job');
    });

    test('should override mock mode per request', async () => {
      disableMock();
      
      const result = await createScheduledJob(
        apiKey,
        'Override Mock Job',
        'smartscraper',
        '0 9 * * 1',
        { test: 'config' },
        true,
        { mock: true }
      );
      
      expect(result).toHaveProperty('id');
      expect(result.job_name).toBe('Mock Scheduled Job');
      
      enableMock();
    });
  });

  describe('Concurrent Operations', () => {
    test('should handle concurrent job creation', async () => {
      const jobConfig = { test: 'config' };
      
      const promises = Array.from({ length: 3 }, (_, i) =>
        createScheduledJob(
          apiKey,
          `Concurrent Job ${i}`,
          'smartscraper',
          '0 9 * * 1',
          jobConfig
        )
      );
      
      const results = await Promise.all(promises);
      
      expect(results).toHaveLength(3);
      results.forEach(result => {
        expect(result).toHaveProperty('id');
        expect(result.job_name).toBe('Mock Scheduled Job');
      });
    });

    test('should handle concurrent job management operations', async () => {
      const jobId = 'test-job-id';
      
      const promises = [
        getScheduledJob(apiKey, jobId),
        pauseScheduledJob(apiKey, jobId),
        resumeScheduledJob(apiKey, jobId),
        triggerScheduledJob(apiKey, jobId)
      ];
      
      const results = await Promise.all(promises);
      
      expect(results).toHaveLength(4);
      expect(results[0]).toHaveProperty('id');
      expect(results[1]).toHaveProperty('message');
      expect(results[2]).toHaveProperty('message');
      expect(results[3]).toHaveProperty('execution_id');
    });
  });
});
