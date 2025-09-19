#!/usr/bin/env node

// Basic test to verify CLI structure and environment
const { isAuthenticated } = require('../lib/config');
const chalk = require('chalk');
const path = require('path');

// Load environment variables
require('dotenv').config({ path: path.resolve(process.cwd(), '.env.local') });

async function runBasicTests() {
  console.log(chalk.blue('🧪 Running basic CLI tests...\n'));

  try {
    // Test 1: Config module loads
    console.log('✅ Config module loads successfully');

    // Test 2: Authentication check works
    const authStatus = await isAuthenticated();
    console.log(`✅ Authentication check works (current status: ${authStatus})`);

    // Test 3: CLI file exists and is executable
    const fs = require('fs');
    const cliPath = path.join(__dirname, '../cli.js');

    if (fs.existsSync(cliPath)) {
      console.log('✅ CLI file exists');

      const stats = fs.statSync(cliPath);
      if (stats.mode & parseInt('111', 8)) {
        console.log('✅ CLI file is executable');
      } else {
        console.log('❌ CLI file is not executable');
      }
    } else {
      console.log('❌ CLI file missing');
    }

    // Test 4: Environment variables
    console.log(chalk.yellow('\n📋 Environment Configuration:'));

    const clientId = process.env.CONNECTED_APP_CLIENT_ID;
    const clientSecret = process.env.CONNECTED_APP_CLIENT_SECRET;
    const projectId = process.env.STYTCH_PROJECT_ID;
    const apiUrl = process.env.API_BASE_URL;

    if (clientId) {
      console.log(`✅ Client ID: ${clientId.substring(0, 20)}...${clientId.substring(clientId.length - 4)}`);
    } else {
      console.log('❌ Client ID: Missing');
    }

    if (clientSecret) {
      console.log(`✅ Client Secret: ${clientSecret.substring(0, 8)}...${clientSecret.substring(clientSecret.length - 4)}`);
    } else {
      console.log('❌ Client Secret: Missing');
    }

    if (projectId) {
      console.log(`✅ Project ID: ${projectId}`);
    } else {
      console.log('❌ Project ID: Missing');
    }

    if (apiUrl) {
      console.log(`✅ API Base URL: ${apiUrl}`);
    } else {
      console.log('❌ API Base URL: Missing (will default to http://localhost:8000)');
    }

    // Test 5: All required env vars present
    const requiredVars = ['CONNECTED_APP_CLIENT_ID', 'CONNECTED_APP_CLIENT_SECRET', 'STYTCH_PROJECT_ID'];
    const missingVars = requiredVars.filter(varName => !process.env[varName]);

    if (missingVars.length === 0) {
      console.log(chalk.green('\n✅ All required environment variables present'));
    } else {
      console.log(chalk.red(`\n❌ Missing environment variables: ${missingVars.join(', ')}`));
    }

    console.log(chalk.green('\n🎉 Basic tests completed!'));

  } catch (error) {
    console.error(chalk.red(`❌ Test failed: ${error.message}`));
    process.exit(1);
  }
}

runBasicTests();