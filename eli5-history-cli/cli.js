#!/usr/bin/env node

const { Command } = require('commander');
const { startAuthFlow } = require('./lib/auth');
const { getExplanationHistory } = require('./lib/api');
const chalk = require('chalk');

const program = new Command();

program
  .name('eli5-history')
  .description('View your Explain Like I\'m 5 explanation history')
  .version('1.0.0');

program
  .command('auth')
  .description('Authenticate with your Eli5 account')
  .action(async () => {
    console.log(chalk.blue('🔐 Starting authentication...'));
    await startAuthFlow();
  });

program
  .command('history')
  .description('Show your explanation history')
  .option('-n, --number <count>', 'number of explanations to show', '10')
  .action(async (options) => {
    console.log(chalk.blue('📚 Fetching your explanation history...'));
    await getExplanationHistory(parseInt(options.number));
  });

program
  .command('status')
  .description('Check authentication status')
  .action(async () => {
    const { isAuthenticated } = require('./lib/config');
    if (await isAuthenticated()) {
      console.log(chalk.green('✅ Authenticated'));
    } else {
      console.log(chalk.red('❌ Not authenticated. Run: eli5-history auth'));
    }
  });

program.parse();