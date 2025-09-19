const { getToken } = require('./config');
const { displayHistory } = require('./display');
const chalk = require('chalk');
const path = require('path');

// Load .env.local
require('dotenv').config({ path: path.resolve(process.cwd(), '.env.local') });

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

async function getExplanationHistory(limit = 10) {
  const token = await getToken();

  if (!token) {
    console.log(chalk.red('❌ Not authenticated. Run: eli5-history auth'));
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/explanations?limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.status === 401) {
      console.log(chalk.red('❌ Authentication expired. Please run: eli5-history auth'));
      return;
    }

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const explanations = await response.json();

    if (!explanations || explanations.length === 0) {
      console.log(chalk.yellow('📝 No explanations found for your organization.'));
      console.log(chalk.gray('Try creating some explanations in the web app first!'));
      return;
    }

    displayHistory(explanations);

  } catch (error) {
    console.error(chalk.red(`❌ Failed to fetch explanations: ${error.message}`));
  }
}

module.exports = { getExplanationHistory };