const open = require('open');
const express = require('express');
const { saveToken } = require('./config');
const chalk = require('chalk');
const path = require('path');

// Load .env.local
require('dotenv').config({ path: path.resolve(process.cwd(), '.env.local') });

const CLIENT_ID = process.env.ELI5_CLI_CLIENT_ID;
const CLIENT_SECRET = process.env.ELI5_CLI_CLIENT_SECRET;
const REDIRECT_URI = 'http://localhost:8080/callback';
const STYTCH_PROJECT_ID = process.env.STYTCH_PROJECT_ID;

async function startAuthFlow() {
  if (!CLIENT_ID || !CLIENT_SECRET) {
    console.error(chalk.red('❌ Missing environment variables. Copy .env.example to .env and fill in your Stytch Connected App credentials.'));
    process.exit(1);
  }

  console.log(chalk.yellow('Opening browser for authentication...'));

  // Construct URL to Eli5 frontend consent page (not directly to Stytch)
  const authUrl = `http://localhost:5173/consent?client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}`;

  open(authUrl);

  // Start local server to catch callback
  const app = express();

  app.get('/callback', async (req, res) => {
    const { code } = req.query;

    if (!code) {
      res.send('❌ Error: No authorization code received');
      console.error(chalk.red('❌ Authentication failed: No code received'));
      process.exit(1);
    }

    try {
      const tokenData = await exchangeCodeForToken(code);
      await saveToken(tokenData.access_token);

      res.send('✅ Success! You can close this window and return to the CLI.');
      console.log(chalk.green('✅ Authentication successful! You can now use eli5-history history'));
      process.exit(0);
    } catch (error) {
      res.send(`❌ Error: ${error.message}`);
      console.error(chalk.red(`❌ Authentication failed: ${error.message}`));
      process.exit(1);
    }
  });

  const server = app.listen(8080, () => {
    console.log(chalk.gray('Waiting for authentication callback...'));
  });

  // Timeout after 5 minutes
  setTimeout(() => {
    server.close();
    console.log(chalk.red('❌ Authentication timeout'));
    process.exit(1);
  }, 300000);
}

async function exchangeCodeForToken(code) {
  const response = await fetch(`https://test.stytch.com/v1/public/${STYTCH_PROJECT_ID}/oauth2/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'authorization_code',
      code,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      redirect_uri: REDIRECT_URI
    })
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(`Token exchange failed: ${response.statusText} - ${errorData.message || 'Unknown error'}`);
  }

  return await response.json();
}

module.exports = { startAuthFlow };