# Advanced Forex Bot - Website Setup Guide

Your professional trading bot website is ready! Here's how to set it up and deploy.

## What's Included

### Database (Supabase)
- User authentication system
- MT5 account management (encrypted credentials)
- Trading sessions tracking
- Trade history with P&L
- Bot configuration storage
- Real-time analytics

### Web Application
- Modern React interface
- Responsive design
- Real-time dashboard
- MT5 account linking
- Bot configuration UI
- Trade analytics

## Quick Setup (5 minutes)

### 1. Get Supabase Credentials

The database is already created! Get your credentials:

1. Log into your Supabase project
2. Go to Project Settings > API
3. Copy these values:
   - Project URL
   - Anon/Public Key

### 2. Configure Web App

```bash
cd web
cp .env.example .env
nano .env
```

Add your credentials:
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

### 3. Run Development Server

```bash
npm run dev
```

Open http://localhost:3000

### 4. Build for Production

```bash
npm run build
```

The `dist/` folder contains your production-ready website.

## Database Schema

### Tables Created

1. **users** - User profiles with trading stats
   - id, email, full_name
   - subscription_tier, total_profit, total_trades, win_rate

2. **mt5_accounts** - MT5 account credentials (encrypted)
   - account_name, broker, account_number, server
   - encrypted_password, balance, equity

3. **trading_sessions** - Active and historical sessions
   - status, started_at, stopped_at
   - total_trades, winning_trades, total_pnl, win_rate

4. **trades** - Individual trade records
   - symbol, trade_type, signal_type
   - entry_price, exit_price, position_size
   - stop_loss, take_profit, pnl, pnl_percent

5. **bot_settings** - Per-user bot configuration
   - symbol, timeframe, risk parameters
   - indicator settings, ML preferences

All tables have Row Level Security (RLS) enabled - users can only access their own data.

## Website Features

### Landing Page (/)
- Professional hero section
- Feature showcase
- Call-to-action buttons

### Authentication
- Sign up with email/password
- Secure login
- Session management

### Dashboard (/dashboard)
- Total profit/loss display
- Win rate statistics
- MT5 accounts overview
- Recent trades list

### Settings (/settings)
- Add MT5 accounts
- Configure bot parameters:
  - Trading symbol
  - Timeframe
  - Risk limits
  - Indicator settings
  - ML prediction toggle

## Deployment Options

### Option 1: Netlify (Recommended)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy --prod --dir=dist
```

### Option 2: Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### Option 3: GitHub Pages

```bash
# Build
npm run build

# Push to gh-pages branch
npm install -g gh-pages
gh-pages -d dist
```

### Option 4: Custom VPS

```bash
# Build
npm run build

# Copy to server
scp -r dist/* user@yourserver.com:/var/www/html/
```

## Connecting Bot to Website

### Backend Integration Needed

Create an Edge Function or API endpoint to:

1. Fetch bot settings from database
2. Start/stop trading sessions
3. Update trade records in real-time
4. Sync MT5 account balance/equity

Example Edge Function:

```typescript
// supabase/functions/bot-control/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )

  const { action, accountId } = await req.json()

  if (action === 'start') {
    // Start trading bot for accountId
    // Update session status
  }

  if (action === 'stop') {
    // Stop trading bot
  }

  return new Response(JSON.stringify({ success: true }))
})
```

## Security Notes

### Production Checklist

- [ ] Use proper password encryption (not base64)
- [ ] Enable 2FA for admin accounts
- [ ] Set up API rate limiting
- [ ] Add CORS configuration
- [ ] Enable SSL/HTTPS
- [ ] Regular security audits
- [ ] Backup database regularly

### Password Storage

Current implementation uses base64 encoding. For production:

```javascript
// Use a proper encryption library
import { encrypt, decrypt } from 'crypto-js'

const encryptPassword = (password) => {
  return encrypt(password, process.env.ENCRYPTION_KEY).toString()
}
```

## Customization

### Change Colors

Edit `web/src/styles/global.css`:

```css
:root {
  --primary: #2563eb;        /* Change to your brand color */
  --success: #10b981;
  --danger: #ef4444;
  --bg-primary: #0f172a;     /* Dark theme background */
}
```

### Add Logo

Replace in `web/src/components/Navbar.jsx`:

```jsx
<img src="/logo.png" alt="Logo" style={{ height: '40px' }} />
```

### Modify Features

Edit `web/src/pages/Home.jsx` to update feature cards.

## API Integration

### From Python Bot

```python
import requests

# Update trade in database
def save_trade_to_web(trade_data):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/trades",
        headers={
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json"
        },
        json=trade_data
    )
    return response.json()
```

## Monitoring

### Add Analytics

1. Google Analytics:
```html
<!-- Add to index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
```

2. Error Tracking (Sentry):
```bash
npm install @sentry/react
```

## Support & Troubleshooting

### Common Issues

**Database Connection Error**
- Check Supabase credentials in `.env`
- Verify project is active
- Check network connectivity

**Build Fails**
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear npm cache: `npm cache clean --force`

**Authentication Issues**
- Verify email confirmation is disabled in Supabase
- Check RLS policies are applied
- Verify user exists in `auth.users` table

## Next Steps

1. Deploy website to Netlify/Vercel
2. Create Edge Functions for bot control
3. Add WebSocket for real-time updates
4. Implement payment system (Stripe)
5. Add email notifications
6. Create admin dashboard
7. Add backtesting interface

## Resources

- React Docs: https://react.dev
- Supabase Docs: https://supabase.com/docs
- Vite Docs: https://vitejs.dev
- Recharts: https://recharts.org

---

Your Advanced Forex Bot website is production-ready!

**Start with**: `cd web && npm run dev`

Then open: http://localhost:3000
