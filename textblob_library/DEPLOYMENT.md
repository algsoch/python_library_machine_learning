# 🚀 Deployment Guide - TextBlob Spell Correction App

This guide explains how to deploy the TextBlob spell correction application to Vercel.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ A GitHub account
- ✅ A Vercel account (free tier works perfectly)
- ✅ Git installed on your machine
- ✅ Project pushed to GitHub repository

## 🔧 Pre-Deployment Checklist

### 1. Verify Project Structure
```
textblob_library/
├── api/
│   └── index.py           ✅ Vercel entry point
├── app.py                  ✅ Flask application (local dev)
├── spell.py                ✅ Core spell correction
├── typo_analyzer.py        ✅ Dataset analyzer
├── requirements.txt        ✅ Dependencies
├── vercel.json            ✅ Vercel configuration
├── templates/
│   └── index.html         ✅ Frontend
├── static/
│   └── main.js            ✅ JavaScript
└── typo.txt               ✅ Dataset
```

### 2. Check `requirements.txt`
Ensure it contains:
```
textblob==0.17.1
flask==3.0.0
```

### 3. Verify `vercel.json`
Should contain:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

## 🚀 Deployment Steps

### Method 1: Deploy via Vercel Dashboard (Recommended)

#### Step 1: Push to GitHub
```powershell
# Navigate to project root
cd f:\machine_learning_technique

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit changes
git commit -m "Add TextBlob spell correction app"

# Push to GitHub
git remote add origin https://github.com/algsoch/python_library_machine_learning.git
git branch -M master
git push -u origin master
```

#### Step 2: Import to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Import your GitHub repository: `algsoch/python_library_machine_learning`
4. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `textblob_library`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

#### Step 3: Configure Environment
No environment variables needed for this project!

#### Step 4: Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes for build to complete
3. Get your live URL: `https://textblob-spell-correction.vercel.app`

### Method 2: Deploy via Vercel CLI

#### Step 1: Install Vercel CLI
```powershell
npm install -g vercel
```

#### Step 2: Login to Vercel
```powershell
vercel login
```

#### Step 3: Deploy
```powershell
cd f:\machine_learning_technique\textblob_library
vercel
```

Follow the prompts:
- **Set up and deploy**: Y
- **Which scope**: Your account
- **Link to existing project**: N
- **Project name**: textblob-spell-correction
- **Directory**: ./
- **Override settings**: N

#### Step 4: Deploy to Production
```powershell
vercel --prod
```

## 🔍 Troubleshooting

### Issue 1: Build Fails - TextBlob Not Found
**Solution**: Ensure `requirements.txt` is in the project root:
```txt
textblob==0.17.1
flask==3.0.0
```

### Issue 2: Static Files Not Loading
**Solution**: Verify `static` and `templates` folders are in the correct location:
```
textblob_library/
├── app.py
├── static/
│   └── main.js
└── templates/
    └── index.html
```

### Issue 3: 404 Error on Routes
**Solution**: Check `vercel.json` routes configuration:
```json
{
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Issue 4: Dataset Not Loading
**Solution**: Ensure `typo.txt` is in the root of `textblob_library/` folder and the path in code is relative:
```python
TYPO_FILE = 'typo.txt'  # Not absolute path
```

### Issue 5: CORS Errors
**Solution**: Add CORS support in `app.py`:
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```

## 📊 Post-Deployment Testing

### 1. Test Main Page
Visit: `https://your-app.vercel.app`
- ✅ Page loads successfully
- ✅ Spell correction form is visible
- ✅ Dataset showcase tabs are functional

### 2. Test API Endpoints
```bash
# Test correction endpoint
curl -X POST https://your-app.vercel.app/api/correct \
  -H "Content-Type: application/json" \
  -d '{"text": "I havv goood speling"}'

# Test dataset stats
curl https://your-app.vercel.app/api/dataset/stats

# Test backend info
curl https://your-app.vercel.app/api/info
```

### 3. Test Frontend Features
- ✅ Spell correction input/output
- ✅ Statistics tab loads
- ✅ Random samples generate
- ✅ Accuracy testing works

## 🔄 Updating Deployment

### Push Updates
```powershell
# Make changes to code
# Then commit and push
git add .
git commit -m "Update: description of changes"
git push

# Vercel automatically redeploys!
```

### Manual Redeploy
1. Go to Vercel Dashboard
2. Select your project
3. Click "Redeploy" on latest deployment

## 🌐 Custom Domain (Optional)

### Add Custom Domain
1. Go to Project Settings → Domains
2. Add your domain: `textblob.yourdomain.com`
3. Add DNS records as instructed by Vercel:
   - Type: CNAME
   - Name: textblob
   - Value: cname.vercel-dns.com

## 📈 Monitoring

### View Deployment Logs
1. Go to Vercel Dashboard
2. Select your project
3. Click "Deployments"
4. Click on specific deployment
5. View "Build Logs" and "Function Logs"

### Analytics
Vercel provides free analytics:
- Page views
- Top pages
- Top referrers
- Response times

## 💰 Cost Estimation

**Vercel Free Tier** (Perfect for this project):
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Serverless function execution
- ✅ Automatic HTTPS
- ✅ Custom domains

**Cost**: $0/month 💸

## 🎯 Performance Optimization

### 1. Enable Caching
Add to `vercel.json`:
```json
{
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### 2. Optimize Dataset Loading
Load dataset on startup (already implemented in `app.py`):
```python
TYPO_DICT = parse_typo_file()
print(f"Loaded {len(TYPO_DICT)} typo entries")
```

### 3. Compress Responses
Add compression middleware in `app.py`:
```python
from flask_compress import Compress
Compress(app)
```

## 🔒 Security Best Practices

1. ✅ No sensitive data in code
2. ✅ HTTPS enabled by default (Vercel)
3. ✅ No environment variables needed
4. ✅ Input validation in place
5. ✅ CORS configured properly

## 📚 Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [TextBlob Documentation](https://textblob.readthedocs.io/)

## 🆘 Support

If you encounter issues:
1. Check [Vercel Documentation](https://vercel.com/docs)
2. Review deployment logs in Vercel Dashboard
3. Test locally first: `python app.py`
4. Ensure all files are committed to Git

## ✅ Deployment Checklist

Before going live:
- [ ] Test locally with `python app.py`
- [ ] Run unit tests: `python -m unittest discover tests`
- [ ] Verify `requirements.txt` is complete
- [ ] Check `vercel.json` configuration
- [ ] Push all changes to GitHub
- [ ] Deploy via Vercel Dashboard
- [ ] Test deployed URL
- [ ] Verify all API endpoints work
- [ ] Test frontend features
- [ ] Update README with live URL

---

**Deployment Time**: ~3-5 minutes  
**Build Time**: ~2-3 minutes  
**Total Time to Live**: ~5-8 minutes

🎉 **Happy Deploying!** 🚀
