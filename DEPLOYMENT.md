# Railway Deployment Guide

This guide will help you deploy the Weighted Assertions Calculator to Railway.

## Prerequisites

1. A GitHub account
2. A Railway account (sign up at [railway.app](https://railway.app))
3. Your code pushed to a GitHub repository

## Deployment Steps

### 1. Prepare Your Repository

Make sure your repository contains these files:
- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `railway.json` - Railway configuration
- `Procfile` - Process file for Railway
- `nixpacks.toml` - Build configuration
- `.gitignore` - Git ignore file

### 2. Deploy to Railway

#### Option A: Deploy from GitHub (Recommended)

1. **Connect to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign in with your GitHub account
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure the Service:**
   - Railway will automatically detect it's a Python/Streamlit app
   - The `railway.json` configuration will be applied automatically
   - No additional configuration needed!

3. **Deploy:**
   - Railway will automatically build and deploy your app
   - You'll get a live URL once deployment is complete

#### Option B: Deploy with Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize and Deploy:**
   ```bash
   railway init
   railway up
   ```

### 3. Configuration Details

The deployment uses these configurations:

#### `railway.json`
- **Builder:** NIXPACKS (automatic Python detection)
- **Start Command:** Streamlit with proper port binding
- **Health Check:** Root path with 100ms timeout
- **Restart Policy:** Auto-restart on failure (max 10 retries)

#### `Procfile`
- Defines the web process for Railway
- Binds to `$PORT` environment variable
- Listens on all interfaces (`0.0.0.0`)

#### `nixpacks.toml`
- Specifies Python 3.9
- Installs dependencies from `requirements.txt`
- Configures the start command

### 4. Environment Variables

Railway will automatically set:
- `PORT` - The port your app should listen on
- `RAILWAY_ENVIRONMENT` - The environment name

### 5. Monitoring and Management

Once deployed, you can:
- **View Logs:** Check the Railway dashboard for real-time logs
- **Monitor Usage:** Track CPU, memory, and network usage
- **Scale:** Adjust resources as needed
- **Restart:** Restart the service if needed
- **Rollback:** Deploy previous versions if issues arise

### 6. Custom Domain (Optional)

1. Go to your project settings in Railway
2. Navigate to "Domains"
3. Add your custom domain
4. Configure DNS records as instructed

### 7. Auto-Deployments

Railway will automatically redeploy when you:
- Push changes to your connected branch
- Merge pull requests (if configured)

## Troubleshooting

### Common Issues

1. **Port Binding Error:**
   - Ensure your app uses `$PORT` environment variable
   - Check that the start command is correct

2. **Build Failures:**
   - Verify all dependencies are in `requirements.txt`
   - Check that Python version is compatible

3. **App Not Starting:**
   - Check logs in Railway dashboard
   - Verify the start command in `railway.json`

### Getting Help

- [Railway Documentation](https://docs.railway.com/)
- [Railway Discord](https://discord.gg/railway)
- [Railway GitHub](https://github.com/railwayapp)

## Cost Optimization

Railway offers:
- **Free Tier:** Limited usage for development
- **Pay-as-you-go:** Scale based on actual usage
- **Auto-sleep:** Apps sleep when inactive (configurable)

Configure auto-sleep in your project settings to optimize costs.

---

**Your app will be live at:** `https://your-project-name.railway.app`

Happy deploying! 🚀
