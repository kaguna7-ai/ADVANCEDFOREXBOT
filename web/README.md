# Advanced Forex Trading Bot - Web Application

Professional web interface for the Advanced Forex Trading Bot with MT5 integration.

## Features

- User authentication with Supabase
- MT5 account management
- Real-time trading dashboard
- Performance analytics
- Bot configuration interface
- Trade history tracking

## Setup

1. Install dependencies:
```bash
cd web
npm install
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your Supabase credentials to `.env`:
```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

4. Start development server:
```bash
npm run dev
```

5. Open http://localhost:3000

## Build for Production

```bash
npm run build
```

## Tech Stack

- React 18
- Vite
- Supabase (Auth + Database)
- React Router
- Recharts (Charts)
- Lucide React (Icons)

## Pages

- `/` - Landing page with features
- `/login` - User login
- `/signup` - User registration
- `/dashboard` - Trading dashboard with stats
- `/settings` - MT5 account management and bot configuration

## Database Tables

- `users` - User profiles
- `mt5_accounts` - MT5 account credentials (encrypted)
- `trading_sessions` - Active and historical sessions
- `trades` - Individual trade records
- `bot_settings` - Bot configuration per user

## Security

- Row Level Security (RLS) enabled on all tables
- Users can only access their own data
- MT5 passwords are base64 encoded (use proper encryption in production)
- Session-based authentication via Supabase
