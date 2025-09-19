const fs = require('fs').promises;
const path = require('path');
const os = require('os');

const CONFIG_DIR = path.join(os.homedir(), '.eli5-history-cli');
const TOKEN_FILE = path.join(CONFIG_DIR, 'token');

async function ensureConfigDir() {
  try {
    await fs.mkdir(CONFIG_DIR, { recursive: true });
  } catch (error) {
    // Directory exists, ignore
  }
}

async function saveToken(token) {
  try {
    await ensureConfigDir();
    await fs.writeFile(TOKEN_FILE, token, 'utf8');
  } catch (error) {
    throw new Error(`Failed to save token: ${error.message}`);
  }
}

async function getToken() {
  try {
    return await fs.readFile(TOKEN_FILE, 'utf8');
  } catch (error) {
    return null; // Token doesn't exist
  }
}

async function clearToken() {
  try {
    await fs.unlink(TOKEN_FILE);
  } catch (error) {
    // Token file doesn't exist, ignore
  }
}

async function isAuthenticated() {
  const token = await getToken();
  return token !== null;
}

module.exports = { saveToken, getToken, clearToken, isAuthenticated };