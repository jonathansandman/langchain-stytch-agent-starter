# Eli5 History CLI

Command-line tool to view your "Explain Like I'm 5" explanation history using Stytch Connected Apps.

## Installation

```bash
git clone [this-repo]
cd eli5-history-cli
npm install
cp .env.example .env.local
# Fill in your environment variables in .env.local
```

## Usage

### Authenticate
```bash
eli5-history auth
# Opens browser for OAuth consent flow
```

### View History
```bash
eli5-history history
# Shows your organization's recent explanations

# Limit results
eli5-history history -n 5
```

### Check Status
```bash
eli5-history status
# Shows authentication status
```

## How It Works

This CLI demonstrates Stytch Connected Apps by:

1. **OAuth Request**: CLI requests permission to access your Eli5 data
2. **User Consent**: You grant permission via browser consent screen
3. **Access Token**: CLI receives token with your organization's permissions
4. **API Access**: CLI uses token to fetch your explanation history

The CLI acts as an external application requesting access to your Eli5 data, demonstrating how third-party apps can integrate with your platform using Stytch Connected Apps.

## Development

### Run Tests
```bash
npm test
```

### Environment Variables
Copy `.env.example` to `.env.local` and fill in:
- `CONNECTED_APP_CLIENT_ID` - From Stytch Connected Apps dashboard
- `CONNECTED_APP_CLIENT_SECRET` - From Stytch Connected Apps dashboard
- `CONNECTED_APP_REDIRECT_URI` - CLI callback URL (default: http://localhost:8080/callback)
- `STYTCH_PROJECT_ID` - Your Stytch project ID
- `API_BASE_URL` - Backend API URL (default: http://localhost:8000)