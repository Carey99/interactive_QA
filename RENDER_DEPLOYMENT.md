# Render Deployment Guide

## 🚀 Deploying Interactive Q&A System to Render

This guide will walk you through deploying your full-stack application to Render.

### 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your code must be in a GitHub repository
3. **Groq API Key**: Get your free API key from [console.groq.com](https://console.groq.com)

### 🔧 Deployment Steps

#### Step 1: Prepare Your Repository

Your repository is already configured with the necessary files:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Process definition
- ✅ `runtime.txt` - Python version
- ✅ `render.yaml` - Render configuration
- ✅ `build.sh` - Build script
- ✅ `start-render.sh` - Start script

#### Step 2: Deploy Backend to Render

1. **Login to Render**: Go to [dashboard.render.com](https://dashboard.render.com)

2. **Create New Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select your `interactive_QA` repository

3. **Configure Service**:
   - **Name**: `interactive-qa-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd server && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free` (for testing)

4. **Set Environment Variables**:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   PYTHON_VERSION=3.12.0
   DEBUG=false
   ENVIRONMENT=production
   ```

5. **Deploy**: Click "Create Web Service"

#### Step 3: Update CORS Origins

Once deployed, update your CORS settings:

1. Get your Render service URL (e.g., `https://interactive-qa-backend.onrender.com`)
2. Update `server/config/settings.py`:
   ```python
   ALLOWED_ORIGINS: str = "http://localhost:3000,https://your-actual-render-url.onrender.com"
   ```
3. Commit and push changes to trigger redeployment

#### Step 4: Deploy Frontend (Optional - Static Site)

For the frontend, you have two options:

**Option A: Deploy Frontend Separately**
1. Create new Static Site on Render
2. **Build Command**: `cd client && npm install && npm run build`
3. **Publish Directory**: `client/out` or `client/.next`

**Option B: Use Current Backend-Only Setup**
- Your backend serves the API
- Use the frontend locally or deploy elsewhere
- Update API URL in frontend to point to Render backend

### 🔍 Testing Your Deployment

1. **Health Check**: Visit `https://your-app.onrender.com/health`
2. **API Docs**: Visit `https://your-app.onrender.com/docs`
3. **Test Endpoint**: 
   ```bash
   curl -X POST https://your-app.onrender.com/api/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "How do I validate my startup idea?"}'
   ```

### 🛠️ Configuration Files Explained

**render.yaml**: Infrastructure as code
**Procfile**: Process definition for deployment
**runtime.txt**: Specifies Python version
**requirements.txt**: Python dependencies

### 🔐 Environment Variables

Set these in Render Dashboard → Service → Environment:

```
GROQ_API_KEY=gsk_your_actual_key_here
DEBUG=false
ENVIRONMENT=production
HOST=0.0.0.0
PORT=10000
```

### 🚨 Troubleshooting

**Common Issues:**

1. **Build Fails**:
   - Check `requirements.txt` includes all dependencies
   - Verify Python version in `runtime.txt`

2. **Service Won't Start**:
   - Check start command in service settings
   - Verify `GROQ_API_KEY` is set correctly

3. **CORS Errors**:
   - Update `ALLOWED_ORIGINS` with your Render URL
   - Ensure frontend points to correct backend URL

4. **API Key Issues**:
   - Verify Groq API key is valid
   - Check key has sufficient credits/quota

### 📊 Monitoring

- **Logs**: View in Render Dashboard → Service → Logs
- **Metrics**: Monitor in Render Dashboard → Service → Metrics
- **Health**: Auto-monitored via `/health` endpoint

### 💰 Costs

- **Free Tier**: 750 hours/month (enough for testing)
- **Paid Plans**: Start at $7/month for production use
- **Sleep Mode**: Free services sleep after 15 minutes of inactivity

### 🔄 Auto-Deploy

Your service will auto-deploy when you push to your main branch. To disable:
- Go to Service Settings → Auto-Deploy → Disable

### 📝 Next Steps After Deployment

1. Test all endpoints thoroughly
2. Update frontend API URLs to point to Render
3. Set up monitoring and alerts
4. Consider upgrading to paid plan for production
5. Set up custom domain (paid feature)

Your Interactive Q&A System is now live on Render! 🎉
