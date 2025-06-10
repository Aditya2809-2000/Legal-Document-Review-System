# ⚖️ Legal Document Review System

An AI-powered legal document analysis system built with Streamlit and Google's Gemini AI.

## 🚀 Features

- Document Overview and Validity Analysis
- Risk Assessment and Compliance Analysis
- Contract Terms and Obligations Analysis
- Legal Language and Clarity Review
- Document Classification and Recommendations
- KPI Analysis and Metrics
- Summary Email Generation

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Get your Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. Run locally: `streamlit run app.py`

## 🌐 Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create new app with `app.py`
4. Add your API key in Settings → Secrets:
   ```toml
   GOOGLE_API_KEY = "your_api_key_here"
   ```
5. Deploy!

## 📁 Files

- `app.py` - Main application
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies
- `style.css` - Custom styling
