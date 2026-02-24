# AI Trip Planner ✈️

An intelligent trip planning application powered by OpenAI agents.

## Features

- AI-powered trip planning with multiple specialized agents
- Budget-aware recommendations
- Local guide insights
- Travel logistics support
- Day-by-day itinerary generation

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run locally:**
   ```bash
   streamlit run streamlit_app.py
   ```

## Deployment on Streamlit Cloud

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add Streamlit app"
   git push
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository, branch, and main file (`streamlit_app.py`)
   - Add your `OPENAI_API_KEY` in the Secrets section (Settings → Secrets)

3. **Share your app:**
   Once deployed, your app will be live at a URL like: `https://ai-planner.streamlit.app`

## Project Structure

- `streamlit_app.py` - Main Streamlit application
- `trip_planner.py` - Core trip planning logic with AI agents
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration