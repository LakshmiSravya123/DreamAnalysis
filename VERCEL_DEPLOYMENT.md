# Neural Dream Weaver - Vercel Deployment Guide

This guide will help you deploy your Neural Dream Weaver application to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. A GitHub account
3. Your Replit project pushed to a GitHub repository
4. A Neon PostgreSQL database (or any PostgreSQL database)
5. An OpenAI API key

## Step 1: Push Your Code to GitHub

1. Create a new repository on GitHub
2. In your Replit workspace, run:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push -u origin main
   ```

## Step 2: Set Up Database

### Option A: Use Neon (Recommended)

1. Go to [neon.tech](https://neon.tech) and create a free account
2. Create a new project
3. Copy your connection string (it should look like: `postgresql://user:password@host/database`)
4. Save this for later - you'll need it for Vercel environment variables

### Option B: Use Your Existing Database

If you already have a PostgreSQL database, make sure:
- It's accessible from the internet (not just localhost)
- You have the full connection string ready

## Step 3: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and log in
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure the project:

   **Framework Preset:** Other
   
   **Root Directory:** `./` (leave as is)
   
   **Build & Output Settings:**
   - These are already configured in `vercel.json` and will be automatically detected
   - Build Command: `vite build`
   - Output Directory: `dist`
   - Install Command: `npm install`
   
   **You don't need to manually set these** - Vercel will read them from vercel.json

5. Click "Environment Variables" and add the following (**ALL REQUIRED**):

   | Name | Value | Description |
   |------|-------|-------------|
   | `DATABASE_URL` | `your-neon-connection-string` | **REQUIRED:** PostgreSQL connection string |
   | `OPENAI_API_KEY` | `your-openai-api-key` | **REQUIRED:** Your OpenAI API key |
   | `JWT_SECRET` | `your-random-secret-key` | **REQUIRED:** A random string for JWT signing (generate one!) |
   | `NODE_ENV` | `production` | Environment mode |

   **⚠️ IMPORTANT: JWT_SECRET is REQUIRED for security**
   
   Generate a secure JWT_SECRET using this command:
   ```bash
   # Run this in terminal:
   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
   ```
   
   **The deployment will fail if JWT_SECRET is not set.** This is intentional to prevent running with an insecure default secret.

6. Click "Deploy"

## Step 4: Run Database Migrations

After your first deployment:

1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Copy your `DATABASE_URL`
4. In your local Replit or terminal, run:
   ```bash
   export DATABASE_URL="your-connection-string"
   npm run db:push
   ```

This will create all necessary database tables.

## Step 5: Verify Deployment

1. Once deployed, Vercel will give you a URL (e.g., `your-app.vercel.app`)
2. Visit your URL to see your app live
3. Test the following features:
   - Dashboard loads correctly
   - Dream analysis works
   - AI companion chat responds
   - Health metrics display

## Architecture Changes for Vercel

Your app has been restructured to work with Vercel's serverless platform:

### Frontend
- Static React SPA served from `dist/public`
- Built with Vite
- No server-side rendering

### Backend
- All Express routes converted to Vercel serverless functions in `/api` directory
- Each API endpoint is a separate serverless function
- Database connections use Neon's serverless driver with connection pooling

### Authentication
- Changed from session-based auth to JWT tokens
- Tokens stored in HttpOnly cookies
- Stateless authentication compatible with serverless

### API Routes

All API endpoints remain the same:
- `GET /api/health-metrics/:userId`
- `POST /api/health-metrics`
- `GET /api/dream-analysis/:userId`
- `POST /api/dream-analysis`
- `GET /api/ai-chat/:userId`
- `POST /api/ai-chat`
- `POST /api/analyze-mood`
- `GET /api/settings/:userId`
- `POST /api/settings/:userId`
- `GET /api/export/:userId`

## Troubleshooting

### Issue: Getting 404 error or blank page
**Solution:** This is usually a SPA routing issue. Make sure `vercel.json` has the catch-all rewrite:
```json
"rewrites": [
  {
    "source": "/api/:path*",
    "destination": "/api/:path*"
  },
  {
    "source": "/(.*)",
    "destination": "/index.html"
  }
]
```
The catch-all `"/(.*)" -> "/index.html"` must come AFTER the API rewrite. Redeploy after fixing.

### Issue: "DATABASE_URL is not defined"
**Solution:** Make sure you added the environment variable in Vercel's project settings and redeployed.

### Issue: "OpenAI API error"
**Solution:** Verify your `OPENAI_API_KEY` is correct and has sufficient credits.

### Issue: "Function execution timeout"
**Solution:** Vercel free tier has a 10-second timeout. OpenAI requests might take longer. Consider upgrading to Pro plan or optimizing API calls.

### Issue: API endpoints returning 404
**Solution:** Make sure all files in the `/api` directory are properly committed to your GitHub repository.

### Issue: Database connection errors
**Solution:** 
- Check that your DATABASE_URL is correct
- Verify your database accepts connections from Vercel's IP ranges
- For Neon: ensure connection pooling is enabled in your connection string

## Updating Your Deployment

To deploy updates:

1. Make changes in your Replit workspace
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```
3. Vercel will automatically redeploy (if auto-deploy is enabled)

## Custom Domain (Optional)

1. Go to your Vercel project
2. Navigate to Settings → Domains
3. Add your custom domain
4. Follow Vercel's DNS configuration instructions

## Cost Considerations

- **Vercel Free Tier:** 
  - 100 GB bandwidth/month
  - Serverless function execution time limits
  - Free SSL certificates
  
- **Neon Free Tier:**
  - 10 GB storage
  - Unlimited compute hours (with some limits)
  
- **OpenAI API:**
  - Pay-per-use based on tokens
  - Monitor usage in OpenAI dashboard

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Review browser console for frontend errors
3. Check Vercel function logs for backend errors
4. Verify all environment variables are set correctly

## Next Steps

- Set up monitoring with Vercel Analytics
- Configure custom domain
- Set up CI/CD for automated testing
- Add error tracking (e.g., Sentry)
- Implement rate limiting for API endpoints
- Add database backups

---

**Note:** The original Express server (`server/index.ts`) is no longer used in Vercel deployment. All backend logic has been moved to serverless functions in the `/api` directory.
