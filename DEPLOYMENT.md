# Deployment Guide

## Quick Deploy to Streamlit Cloud

### Step 1: Prepare Your GitHub Repository

1. Create a new repository on GitHub
2. Initialize git in your local project:
   ```bash
   cd streamlit_investor_dashboard
   git init
   git add .
   git commit -m "Initial commit: AI Datacenter investor dashboard"
   ```
3. Connect to GitHub and push:
   ```bash
   git remote add origin https://github.com/yourusername/ai-datacenter-dashboard.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in the deployment form:
   - **Repository:** yourusername/ai-datacenter-dashboard
   - **Branch:** main
   - **Main file path:** app.py
5. Click "Deploy!"

Your app will be live at: `https://yourusername-ai-datacenter-dashboard.streamlit.app`

### Step 3: Configure (Optional)

Add secrets if needed in the Streamlit Cloud dashboard:
1. Go to your app settings
2. Click "Secrets"
3. Add any API keys or sensitive configuration

## Local Development

### Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```

### Test
Open browser to: `http://localhost:8501`

## Alternative Deployment Options

### Heroku

1. Create `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   " > ~/.streamlit/config.toml
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Docker

1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py"]
   ```

2. Build and run:
   ```bash
   docker build -t investor-dashboard .
   docker run -p 8501:8501 investor-dashboard
   ```

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
streamlit run app.py --server.port 8502
```

**Module not found:**
```bash
pip install -r requirements.txt --upgrade
```

**Data files not loading:**
- Verify all CSV files are in `/data` directory
- Check file paths in Python code use `Path` correctly

## Performance Optimization

1. **Use caching** - Already implemented with `@st.cache_data`
2. **Minimize data loading** - Load data once at page level
3. **Optimize charts** - Plotly charts are already optimized

## Security Notes

- Never commit API keys or passwords
- Use Streamlit secrets for sensitive data
- Restrict dashboard access if needed (Streamlit Cloud paid tier)
- Review data privacy before deploying

---

For questions: support@aidcvancouver.com
