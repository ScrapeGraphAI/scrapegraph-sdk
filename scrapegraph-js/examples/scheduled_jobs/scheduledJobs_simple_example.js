import {
  createScheduledJob,
  getScheduledJobs,
  getScheduledJob,
  updateScheduledJob,
  deleteScheduledJob,
  pauseScheduledJob,
  resumeScheduledJob,
  triggerScheduledJob,
  getJobExecutions,
  enableMock,
  disableMock
} from '../index.js';

/**
 * Simple scheduled jobs example for JavaScript SDK
 */
async function simpleScheduledJobsExample() {
  const apiKey = process.env.SGAI_API_KEY || 'your-api-key-here';
  
  if (apiKey === 'your-api-key-here') {
    console.log('❌ Error: SGAI_API_KEY environment variable not set');
    console.log('Please either:');
    console.log('  1. Set environment variable: export SGAI_API_KEY="your-api-key-here"');
    console.log('  2. Or update the apiKey variable in this script');
    return;
  }
  
  console.log('🚀 Starting Simple Scheduled Jobs Example');
  console.log('='.repeat(50));
  
  const jobIds = [];
  
  try {
    // Create a SmartScraper job
    console.log('\n📅 Creating SmartScraper job...');
    const smartScraperJob = await createScheduledJob(
      apiKey,
      'Daily News Scraper',
      'smartscraper',
      '0 9 * * *', // Daily at 9 AM
      {
        website_url: 'https://news.ycombinator.com',
        user_prompt: 'Extract the top 5 news titles and their URLs',
        render_heavy_js: false
      },
      true
    );
    
    console.log(`✅ Created SmartScraper job: ${smartScraperJob.id}`);
    jobIds.push(smartScraperJob.id);
    
    // Create a SearchScraper job
    console.log('\n📅 Creating SearchScraper job...');
    const searchScraperJob = await createScheduledJob(
      apiKey,
      'Weekly AI Research',
      'searchscraper',
      '0 10 * * 1', // Every Monday at 10 AM
      {
        user_prompt: 'Find the latest AI and machine learning research papers',
        num_results: 5
      },
      true
    );
    
    console.log(`✅ Created SearchScraper job: ${searchScraperJob.id}`);
    jobIds.push(searchScraperJob.id);
    
    // List all jobs
    console.log('\n📋 Listing all scheduled jobs:');
    const allJobs = await getScheduledJobs(apiKey, { page: 1, pageSize: 10 });
    console.log(`Total jobs: ${allJobs.total}`);
    
    allJobs.jobs.forEach(job => {
      console.log(`  - ${job.job_name} (${job.service_type}) - Active: ${job.is_active}`);
    });
    
    // Get details of first job
    if (jobIds.length > 0) {
      console.log(`\n🔍 Getting details for job ${jobIds[0]}:`);
      const jobDetails = await getScheduledJob(apiKey, jobIds[0]);
      console.log(`  Name: ${jobDetails.job_name}`);
      console.log(`  Cron: ${jobDetails.cron_expression}`);
      console.log(`  Next run: ${jobDetails.next_run_at || 'N/A'}`);
      
      // Update the job
      console.log(`\n📝 Updating job ${jobIds[0]}:`);
      const updatedJob = await updateScheduledJob(apiKey, jobIds[0], {
        jobName: 'Updated Daily News Scraper',
        cronExpression: '0 8 * * *' // Change to 8 AM
      });
      console.log(`  Updated name: ${updatedJob.job_name}`);
      console.log(`  Updated cron: ${updatedJob.cron_expression}`);
      
      // Pause the job
      console.log(`\n⏸️ Pausing job ${jobIds[0]}:`);
      const pauseResult = await pauseScheduledJob(apiKey, jobIds[0]);
      console.log(`  Status: ${pauseResult.message}`);
      
      // Resume the job
      console.log(`\n▶️ Resuming job ${jobIds[0]}:`);
      const resumeResult = await resumeScheduledJob(apiKey, jobIds[0]);
      console.log(`  Status: ${resumeResult.message}`);
      
      // Trigger the job manually
      console.log(`\n🚀 Manually triggering job ${jobIds[0]}:`);
      const triggerResult = await triggerScheduledJob(apiKey, jobIds[0]);
      console.log(`  Execution ID: ${triggerResult.execution_id}`);
      console.log(`  Message: ${triggerResult.message}`);
      
      // Get execution history
      console.log(`\n📊 Getting execution history for job ${jobIds[0]}:`);
      const executions = await getJobExecutions(apiKey, jobIds[0], { page: 1, pageSize: 5 });
      console.log(`  Total executions: ${executions.total}`);
      
      executions.executions.slice(0, 3).forEach(execution => {
        console.log(`    - Execution ${execution.id}: ${execution.status}`);
        console.log(`      Started: ${execution.started_at}`);
        if (execution.completed_at) {
          console.log(`      Completed: ${execution.completed_at}`);
        }
        if (execution.credits_used) {
          console.log(`      Credits used: ${execution.credits_used}`);
        }
      });
    }
    
  } catch (error) {
    console.error('❌ Error during execution:', error.message);
  } finally {
    // Clean up created jobs
    console.log('\n🧹 Cleaning up created jobs:');
    for (const jobId of jobIds) {
      try {
        const deleteResult = await deleteScheduledJob(apiKey, jobId);
        console.log(`  ✅ Deleted job ${jobId}: ${deleteResult.message}`);
      } catch (error) {
        console.error(`  ❌ Failed to delete job ${jobId}:`, error.message);
      }
    }
  }
  
  console.log('\n✅ Simple Scheduled Jobs Example completed!');
}

/**
 * Mock mode example
 */
async function mockModeExample() {
  console.log('\n🧪 Mock Mode Example');
  console.log('='.repeat(30));
  
  // Enable mock mode
  enableMock();
  
  const apiKey = 'mock-api-key';
  
  try {
    // Create a job in mock mode
    const mockJob = await createScheduledJob(
      apiKey,
      'Mock Job',
      'smartscraper',
      '0 9 * * *',
      { test: 'config' },
      true
    );
    
    console.log(`✅ Created mock job: ${mockJob.id}`);
    console.log(`  Job name: ${mockJob.job_name}`);
    console.log(`  Service type: ${mockJob.service_type}`);
    
    // List jobs in mock mode
    const mockJobs = await getScheduledJobs(apiKey);
    console.log(`📋 Mock jobs count: ${mockJobs.total}`);
    
    // Trigger job in mock mode
    const triggerResult = await triggerScheduledJob(apiKey, mockJob.id);
    console.log(`🚀 Mock trigger result: ${triggerResult.message}`);
    
  } catch (error) {
    console.error('❌ Mock mode error:', error.message);
  } finally {
    disableMock();
  }
  
  console.log('✅ Mock Mode Example completed!');
}

/**
 * Concurrent operations example
 */
async function concurrentOperationsExample() {
  console.log('\n⚡ Concurrent Operations Example');
  console.log('='.repeat(40));
  
  const apiKey = process.env.SGAI_API_KEY || 'your-api-key-here';
  
  if (apiKey === 'your-api-key-here') {
    console.log('❌ Error: SGAI_API_KEY environment variable not set');
    return;
  }
  
  const jobIds = [];
  
  try {
    // Create multiple jobs concurrently
    console.log('📅 Creating multiple jobs concurrently...');
    
    const jobPromises = [
      createScheduledJob(
        apiKey,
        'Concurrent Job 1',
        'smartscraper',
        '0 9 * * *',
        { website_url: 'https://example1.com', user_prompt: 'Extract data' }
      ),
      createScheduledJob(
        apiKey,
        'Concurrent Job 2',
        'searchscraper',
        '0 10 * * *',
        { user_prompt: 'Find information', num_results: 3 }
      ),
      createScheduledJob(
        apiKey,
        'Concurrent Job 3',
        'smartscraper',
        '0 11 * * *',
        { website_url: 'https://example2.com', user_prompt: 'Monitor changes' }
      )
    ];
    
    const results = await Promise.all(jobPromises);
    
    results.forEach((result, index) => {
      console.log(`  ✅ Created job ${index + 1}: ${result.id}`);
      jobIds.push(result.id);
    });
    
    // Trigger all jobs concurrently
    console.log('\n🚀 Triggering all jobs concurrently...');
    
    const triggerPromises = jobIds.map(jobId => triggerScheduledJob(apiKey, jobId));
    const triggerResults = await Promise.all(triggerPromises);
    
    triggerResults.forEach((result, index) => {
      console.log(`  ✅ Triggered job ${index + 1}: ${result.execution_id}`);
    });
    
    // Get execution history for all jobs concurrently
    console.log('\n📊 Getting execution history for all jobs...');
    
    const executionPromises = jobIds.map(jobId => getJobExecutions(apiKey, jobId));
    const executionResults = await Promise.all(executionPromises);
    
    executionResults.forEach((result, index) => {
      console.log(`  📈 Job ${index + 1} executions: ${result.total}`);
    });
    
  } catch (error) {
    console.error('❌ Concurrent operations error:', error.message);
  } finally {
    // Clean up all jobs
    console.log('\n🧹 Cleaning up all jobs...');
    const deletePromises = jobIds.map(jobId => deleteScheduledJob(apiKey, jobId));
    await Promise.allSettled(deletePromises);
    console.log('✅ Cleanup completed');
  }
  
  console.log('✅ Concurrent Operations Example completed!');
}

/**
 * Main function to run all examples
 */
async function main() {
  try {
    await simpleScheduledJobsExample();
    await mockModeExample();
    await concurrentOperationsExample();
  } catch (error) {
    console.error('❌ Main execution error:', error.message);
  }
}

// Run the examples
main().catch(console.error);
