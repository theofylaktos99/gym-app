# 🚀 Render.com Deployment Guide

Deploy your Gym SaaS application to Render.com and get a live link in minutes!

## 🌐 What is Render?

Render is a cloud platform that makes it easy to deploy web applications, databases, and more. It offers:
- **Free tier** for testing and small projects
- **Automatic deployments** from GitHub
- **Managed PostgreSQL** database
- **SSL certificates** (HTTPS) included
- **EU data centers** (Frankfurt, perfect for Greece!)

## ⚡ Quick Deploy (5 Minutes)

### Prerequisites
- GitHub account with this repository
- Render.com account (free signup at [render.com](https://render.com))

### Deployment Steps

#### 1. **Connect to Render**

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select this repository: `theofylaktos99/gym-app`
5. Select the branch: `copilot/recreate-saas-application`

#### 2. **Configure Blueprint**

Render will automatically detect `render.yaml` and create:
- ✅ Web Service (Flask app)
- ✅ PostgreSQL Database

Click **"Apply"** to start deployment.

#### 3. **Wait for Deployment**

- Database: ~2-3 minutes
- Web Service: ~3-5 minutes
- Total: ~5-8 minutes

#### 4. **Access Your Live App**

Once deployed, Render provides a URL like:
```
https://gym-saas-app.onrender.com
```

**Your app is now live! 🎉**

## 🔑 Demo Login Credentials

After deployment, use these credentials:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Member | `123456` | `654321` |
| Staff | `staff` | `staff123` |

## ⚙️ Configuration

### Environment Variables

Render automatically configures:
- `FLASK_ENV=production`
- `SECRET_KEY` (auto-generated secure key)
- `JWT_SECRET_KEY` (auto-generated secure key)
- `DATABASE_URL` (PostgreSQL connection string)

### Custom Configuration

To add custom environment variables:

1. Go to your service in Render dashboard
2. Click **"Environment"** tab
3. Add variables:
   - `SEED_DEMO_DATA=true` (to load demo data on first deploy)
   - `PORT` (auto-configured by Render)

## 📊 Database Management

### Access PostgreSQL

1. In Render dashboard, go to your database
2. Click **"Connect"** to get connection details
3. Use external connection or internal connection URL

### Run Migrations

Migrations run automatically during build. To run manually:

1. Go to service → **"Shell"** tab
2. Run:
```bash
flask db upgrade
```

### Seed Demo Data

To populate with demo data:

1. Add environment variable: `SEED_DEMO_DATA=true`
2. Trigger manual deploy or wait for next auto-deploy
3. Or use Shell:
```bash
python run.py seed_demo_data
```

## 🔄 Updates & Deployments

### Automatic Deployments

Render auto-deploys when you push to GitHub:

```bash
git push origin copilot/recreate-saas-application
```

Wait 2-3 minutes, and your changes are live!

### Manual Deployment

1. Go to service in Render dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

## 📈 Scaling

### Free Tier Limits

- 750 hours/month of web service
- PostgreSQL: 90 days free trial, then $7/month
- 512 MB RAM
- Sleeps after 15 min of inactivity (wakes on request)

### Upgrade Plans

For production use:

1. **Starter**: $7/month - Always on, more resources
2. **Standard**: $25/month - Horizontal scaling, monitoring
3. **Pro**: $85/month - Advanced features

## 🌍 Multiple Deployments

Deploy different versions:

### Production
- Branch: `main`
- URL: `gym-saas-app.onrender.com`

### Staging
- Branch: `copilot/recreate-saas-application`
- URL: `gym-saas-app-staging.onrender.com`

### Development
- Branch: `develop`
- URL: `gym-saas-app-dev.onrender.com`

## 🔐 Security

### HTTPS

✅ Automatic SSL certificates (HTTPS enabled by default)

### Database Security

✅ PostgreSQL with encrypted connections
✅ Automatic backups (paid plans)
✅ Database credentials in environment variables

### App Security

✅ Secret keys auto-generated
✅ Environment variables not exposed
✅ Security headers (configure in Flask)

## 🛠️ Troubleshooting

### Service Won't Start

Check logs in Render dashboard:
1. Go to service → **"Logs"** tab
2. Look for errors in build or deploy logs

Common issues:
- **Database not ready**: Wait 1-2 minutes after DB creation
- **Migration failed**: Check if migrations folder exists
- **Import errors**: Check requirements.txt has all dependencies

### Database Connection Error

1. Verify DATABASE_URL environment variable is set
2. Check database is running (green status in dashboard)
3. Restart service if needed

### App Sleeping (Free Tier)

Free tier sleeps after 15 min inactivity:
- First request after sleep: 30-60 seconds to wake
- Solution: Upgrade to Starter plan ($7/month) for always-on

## 📱 Custom Domain

### Add Your Domain

1. In service → **"Settings"** → **"Custom Domain"**
2. Add your domain (e.g., `gym.yourdomain.com`)
3. Update DNS records as shown by Render
4. Wait for DNS propagation (5-60 minutes)

### Example

```
CNAME record:
gym.yourdomain.com → gym-saas-app.onrender.com
```

## 🔄 CI/CD Pipeline

Render provides automatic CI/CD:

```
Push to GitHub → Render detects → Build → Test → Deploy → Live!
```

### Build Process

1. Install dependencies (`pip install -r requirements.txt`)
2. Run migrations (`flask db upgrade`)
3. Seed data if configured
4. Start Gunicorn server

## 📊 Monitoring

### Health Checks

Render automatically monitors:
- HTTP endpoint: `/` (returns 200 OK)
- Restarts if unhealthy

### View Logs

Real-time logs in Render dashboard:
```
Service → Logs → Live log tail
```

### Metrics (Paid Plans)

- CPU usage
- Memory usage
- Request rate
- Response time

## 🌐 Multi-Region

For global deployment:

1. Deploy in Frankfurt (Europe) - Good for Greece
2. Deploy in Oregon (US West)
3. Deploy in Singapore (Asia)

Use Cloudflare or similar CDN for global traffic routing.

## 💡 Best Practices

### For Production

1. **Use Starter plan** ($7/month) - Always on, no sleep
2. **Enable auto-deploy** - Continuous deployment from GitHub
3. **Configure alerts** - Get notified of issues
4. **Use custom domain** - Professional appearance
5. **Backup database** - Regular backups (manual or paid plan)

### For Development

1. **Use free tier** - Great for testing
2. **Separate environments** - dev/staging/prod
3. **Test before merging** - Deploy feature branches
4. **Monitor logs** - Check for errors regularly

## 📞 Support

### Render Support

- Documentation: [render.com/docs](https://render.com/docs)
- Community: [community.render.com](https://community.render.com)
- Status: [status.render.com](https://status.render.com)

### Gym SaaS Support

- See [README_SAAS.md](README_SAAS.md) for app documentation
- See [QUICKSTART.md](QUICKSTART.md) for local setup
- See [ARCHITECTURE.md](ARCHITECTURE.md) for system design

## 🎯 Quick Reference

### Render Dashboard URLs

- **Services**: https://dashboard.render.com/
- **Databases**: https://dashboard.render.com/databases
- **Blueprints**: https://dashboard.render.com/blueprints

### Useful Commands (in Render Shell)

```bash
# Check app status
python -c "from app import create_app; print('App OK')"

# Run migrations
flask db upgrade

# Seed demo data
python run.py seed_demo_data

# Check database
python -c "from app import db; print(db.engine.url)"

# Create admin user
flask shell
>>> from app.models import User, Tenant
>>> # Create user commands here
```

## 🎉 Success!

Your Gym SaaS application is now:
- ✅ Live on the internet
- ✅ HTTPS enabled
- ✅ Auto-deploys from GitHub
- ✅ Professional URL
- ✅ Scalable infrastructure

Share your link with gym owners and start selling! 🏋️‍♂️

---

**Live URL**: `https://gym-saas-app.onrender.com`

**Next Steps**:
1. Share the link
2. Test all features
3. Add custom domain (optional)
4. Upgrade to paid plan for production (recommended)
