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

// Enable mock mode for testing
enableMock();

/**
 * Create a SmartScraper scheduled job
 */
async function createSmartScraperJob(apiKey) {
  console.log('📅 Creating SmartScraper scheduled job...');
  
  const jobConfig = {
    website_url: 'https://news.ycombinator.com',
    user_prompt: 'Extract the top 5 news titles and their URLs',
    render_heavy_js: false,
    headers: {
      'User-Agent': 'Mozilla/5.0 (compatible; ScheduledJob/1.0)'
    }
  };
  
  try {
    const result = await createScheduledJob(
      apiKey,
      'HN Top News Scraper',
      'smartscraper',
      '0 */6 * * *', // Every 6 hours
      jobConfig,
      true
    );
    
    console.log(`✅ Created SmartScraper job with ID: ${result.id}`);
    return result.id;
  } catch (error) {
    console.error('❌ Error creating SmartScraper job:', error.message);
    throw error;
  }
}

/**
 * Create a SearchScraper scheduled job
 */
async function createSearchScraperJob(apiKey) {
  console.log('📅 Creating SearchScraper scheduled job...');
  
  const jobConfig = {
    user_prompt: 'Find the latest AI and machine learning news',
    num_results: 5,
    headers: {
      'User-Agent': 'Mozilla/5.0 (compatible; ScheduledJob/1.0)'
    }
  };
  
  try {
    const result = await createScheduledJob(
      apiKey,
      'AI News Search',
      'searchscraper',
      '0 9 * * 1', // Every Monday at 9 AM
      jobConfig,
      true
    );
    
    console.log(`✅ Created SearchScraper job with ID: ${result.id}`);
    return result.id;
  } catch (error) {
    console.error('❌ Error creating SearchScraper job:', error.message);
    throw error;
  }
}

/**
 * Create a Crawl scheduled job
 */
async function createCrawlJob(apiKey) {
  console.log('📅 Creating Crawl scheduled job...');
  
  const jobConfig = {
    url: 'https://example.com',
    prompt: 'Extract all product information',
    extraction_mode: true,
    depth: 2,
    max_pages: 10,
    same_domain_only: true,
    cache_website: true
  };
  
  try {
    const result = await createScheduledJob(
      apiKey,
      'Product Catalog Crawler',
      'crawl',
      '0 2 * * *', // Daily at 2 AM
      jobConfig,
      true
    );
    
    console.log(`✅ Created Crawl job with ID: ${result.id}`);
    return result.id;
  } catch (error) {
    console.error('❌ Error creating Crawl job:', error.message);
    throw error;
  }
}

/**
 * Manage scheduled jobs
 */
async function manageJobs(apiKey, jobIds) {
  console.log('\n🔧 Managing scheduled jobs...');
  
  try {
    // List all jobs
    console.log('\n📋 Listing all scheduled jobs:');
    const jobsResult = await getScheduledJobs(apiKey, { page: 1, pageSize: 10 });
    console.log(`Total jobs: ${jobsResult.total}`);
    
    jobsResult.jobs.forEach(job => {
      console.log(`  - ${job.job_name} (${job.service_type}) - Active: ${job.is_active}`);
    });
    
    // Get details of first job
    if (jobIds.length > 0) {
      console.log(`\n🔍 Getting details for job ${jobIds[0]}:`);
      const jobDetails = await getScheduledJob(apiKey, jobIds[0]);
      console.log(`  Name: ${jobDetails.job_name}`);
      console.log(`  Cron: ${jobDetails.cron_expression}`);
      console.log(`  Next run: ${jobDetails.next_run_at || 'N/A'}`);
      
      // Pause the first job
      console.log(`\n⏸️ Pausing job ${jobIds[0]}:`);
      const pauseResult = await pauseScheduledJob(apiKey, jobIds[0]);
      console.log(`  Status: ${pauseResult.message}`);
      
      // Resume the job
      console.log(`\n▶️ Resuming job ${jobIds[0]}:`);
      const resumeResult = await resumeScheduledJob(apiKey, jobIds[0]);
      console.log(`  Status: ${resumeResult.message}`);
      
      // Update job configuration
      console.log(`\n📝 Updating job ${jobIds[0]}:`);
      const updateResult = await updateScheduledJob(apiKey, jobIds[0], {
        jobName: 'Updated HN News Scraper',
        cronExpression: '0 */4 * * *' // Every 4 hours instead of 6
      });
      console.log(`  Updated job name: ${updateResult.job_name}`);
      console.log(`  Updated cron: ${updateResult.cron_expression}`);
    }
  } catch (error) {
    console.error('❌ Error managing jobs:', error.message);
  }
}

/**
 * Trigger and monitor jobs
 */
async function triggerAndMonitorJobs(apiKey, jobIds) {
  console.log('\n🚀 Triggering and monitoring jobs...');
  
  for (const jobId of jobIds) {
    try {
      console.log(`\n🎯 Manually triggering job ${jobId}:`);
      const triggerResult = await triggerScheduledJob(apiKey, jobId);
      const executionId = triggerResult.execution_id;
      console.log(`  Execution ID: ${executionId}`);
      console.log(`  Message: ${triggerResult.message}`);
      
      // Wait a bit for execution to start
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Get execution history
      console.log(`\n📊 Getting execution history for job ${jobId}:`);
      const executions = await getJobExecutions(apiKey, jobId, { page: 1, pageSize: 5 });
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
    } catch (error) {
      console.error(`❌ Error triggering job ${jobId}:`, error.message);
    }
  }
}

/**
 * Clean up created jobs
 */
async function cleanupJobs(apiKey, jobIds) {
  console.log('\n🧹 Cleaning up created jobs...');
  
  for (const jobId of jobIds) {
    try {
      console.log(`🗑️ Deleting job ${jobId}:`);
      const deleteResult = await deleteScheduledJob(apiKey, jobId);
      console.log(`  Status: ${deleteResult.message}`);
    } catch (error) {
      console.error(`❌ Error deleting job ${jobId}:`, error.message);
    }
  }
}

/**
 * Main function demonstrating scheduled jobs
 */
async function main() {
  const apiKey = process.env.SGAI_API_KEY || 'your-api-key-here';
  
  if (apiKey === 'your-api-key-here') {
    console.log('❌ Error: SGAI_API_KEY environment variable not set');
    console.log('Please either:');
    console.log('  1. Set environment variable: export SGAI_API_KEY="your-api-key-here"');
    console.log('  2. Or update the apiKey variable in this script');
    return;
  }
  
  console.log('🚀 Starting Scheduled Jobs Demo');
  console.log('='.repeat(50));
  
  const jobIds = [];
  
  try {
    // Create different types of scheduled jobs
    const smartscraperJobId = await createSmartScraperJob(apiKey);
    jobIds.push(smartscraperJobId);
    
    const searchscraperJobId = await createSearchScraperJob(apiKey);
    jobIds.push(searchscraperJobId);
    
    const crawlJobId = await createCrawlJob(apiKey);
    jobIds.push(crawlJobId);
    
    // Manage jobs
    await manageJobs(apiKey, jobIds);
    
    // Trigger and monitor jobs
    await triggerAndMonitorJobs(apiKey, jobIds);
    
  } catch (error) {
    console.error('❌ Error during execution:', error.message);
  } finally {
    // Clean up
    await cleanupJobs(apiKey, jobIds);
  }
  
  console.log('\n✅ Scheduled Jobs Demo completed!');
}

// Run the demo
main().catch(console.error);
