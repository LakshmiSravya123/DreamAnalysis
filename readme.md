# Neural Dream Weaver

## Description
Neural Dream Weaver is a Streamlit-based web application simulating a Brain-Computer Interface (BCI) system for dream analysis, mood tracking, and health monitoring. It uses simulated data for health metrics (heart rate, stress levels, daily steps, sleep duration) and neural signals, as no real-time BCI or health data is publicly available from OpenAI or similar sources. The app integrates OpenAI’s Realtime API (via Chat Completions with `gpt-4o-mini`) for real-time analysis of user-provided text inputs (e.g., dream descriptions or mood journals), offering emotion detection and dream interpretation. This enhanced version features a modern UI with light/dark themes, responsive design, data export, and improved simulations for realism.

## Features
- **Dashboard**: Displays real-time simulated metrics (heart rate, stress, mood), a 7-day mood timeline, sleep/dream activity charts, and a text input section for OpenAI-powered mood/dream analysis.
- **Real-Time Monitoring**: Visualizes simulated EEG brain waves (alpha, beta) and a neural network graph of brain region connections.
- **Health Analytics**: Interactive charts for selected metrics, correlation matrix, and personalized insights based on simulated data correlations.
- **Dream Analysis**: Visualizes dream symbol frequencies and emotion intensities using pie charts and histograms, with OpenAI-driven interpretation of the latest dream.
- **AI Companion**: A chat interface for real-time interaction, using OpenAI to analyze user text for emotions and provide contextual responses. Includes quick wellness actions (breathing exercise, meditation, mood check).
- **Settings**: Configurable BCI parameters (electrode count, alerts) and theme toggle (light/dark) with session persistence.
- **Data Export**: Download simulated data as a CSV file.
- **Theme Support**: Light and dark modes, persisted via session state for a consistent user experience.
- **Error Handling**: Graceful handling of missing API keys or OpenAI API errors, with manual key input as a fallback.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. **Install Dependencies**:
   Ensure Python 3.8+ is installed, then install required packages:
   ```bash
   pip install streamlit pandas numpy plotly networkx openai
   ```
3. **Set Up OpenAI API Key**:
   - Obtain an API key from https://platform.openai.com/account/api-keys.
   - Create a `.streamlit/secrets.toml` file in the project directory:
     ```bash
     mkdir .streamlit
     touch .streamlit/secrets.toml
     ```
   - Add the key to `secrets.toml`:
     ```toml
     # .streamlit/secrets.toml
     OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
     ```
   - Add `.streamlit/secrets.toml` to `.gitignore` to prevent committing sensitive data:
     ```bash
     echo ".streamlit/secrets.toml" >> .gitignore
     ```
   - Alternatively, set the key as an environment variable:
     ```bash
     export OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
     ```

## Usage
1. **Run the App Locally**:
   ```bash
   streamlit run improved_dreamandmood_openai.py
   ```
2. **Navigate the App**:
   - Use the sidebar to switch between sections: Dashboard, Real-Time Monitoring, Health Analytics, Dream Analysis, AI Companion, and Settings.
   - In the **Dashboard** or **AI Companion**, enter text (e.g., “I dreamed of flying over a calm ocean”) to trigger OpenAI’s real-time analysis for emotions or dream interpretation.
   - Explore visualizations (mood timelines, health metrics, dream patterns) and interact with settings or wellness actions.
3. **Data Simulation**:
   - The app generates synthetic data for January 1–30, 2024, with hourly entries for heart rate, stress, steps, sleep, mood, and dreams, using realistic patterns (e.g., circadian rhythms, workday stress).
   - Rerun the app to generate new simulated data.
4. **Session Persistence**:
   - Chat history, settings, and theme preferences are stored in Streamlit’s session state and persist during the session.
5. **Export Data**:
   - Use the “Download Data” button in the Dashboard to export the simulated dataset as a CSV file.

## Project Structure
- `improved_dreamandmood_openai.py`: Main application script with all functionality.
- `.streamlit/secrets.toml`: Stores sensitive data like the OpenAI API key (not committed to version control).
- `.gitignore`: Ensures `secrets.toml` and other sensitive files are excluded from Git.

## Dependencies
- **streamlit**: Web app framework for the UI.
- **pandas**, **numpy**: Data manipulation and simulation.
- **plotly**: Interactive visualizations (charts, graphs).
- **networkx**: Neural network graph generation.
- **openai**: Integration with OpenAI’s Realtime API for text-based mood and dream analysis.

## Limitations
- **Simulated Data**: Health and neural metrics (heart rate, stress, steps, sleep, brain waves) are simulated, as OpenAI and other public sources (e.g., Neurable, Hugging Face) do not provide real-time BCI/health data feeds.
- **OpenAI Dependency**: Real-time mood/dream analysis requires a valid OpenAI API key and incurs API usage costs (e.g., ~$0.15/1K tokens for `gpt-4o-mini`). See https://openai.com/api/pricing for details.
- **Not for Medical Use**: The app is a demo and not intended for clinical or diagnostic purposes.
- **Session-Based Persistence**: Chat history and settings reset when the session ends or the app is restarted.
- **Randomness**: Simulated data varies on each run, which may affect consistency for testing.

## Deployment
To deploy on **Streamlit Community Cloud** or similar platforms:
1. Push the code to a GitHub repository (ensure `.streamlit/secrets.toml` is in `.gitignore`).
2. Connect the repository to Streamlit Cloud (https://share.streamlit.io).
3. Add the OpenAI API key in the Streamlit Cloud dashboard under **Settings > Secrets**:
   ```toml
   OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
   ```
4. Deploy the app and access it via the provided URL.

For other platforms (e.g., Heroku, AWS), set `OPENAI_API_KEY` as an environment variable:
```bash
heroku config:set OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Focus areas for contributions:
- Integrating real BCI data (e.g., via Neurable’s developer kit, if available).
- Enhancing visualizations or adding new analytics.
- Improving OpenAI API interactions (e.g., handling audio inputs with Realtime API).
- Adding user authentication or persistent storage.

## Troubleshooting
- **“OpenAI API key required” Error**:
  - Verify `secrets.toml` exists and contains the correct key.
  - Ensure the key starts with `sk-` and is valid (test via OpenAI’s API playground).
  - Check file permissions for `.streamlit/secrets.toml`.
- **Visualization Issues**:
  - Ensure all dependencies (`plotly`, `networkx`) are installed.
  - Clear Streamlit cache (`streamlit cache clear`) if charts don’t render.
- **Deployment Errors**:
  - Confirm secrets are set in the platform’s environment settings.
  - Check logs for dependency or API issues.

## License
MIT License. See `LICENSE` file for details.

## Acknowledgments
- Built with Streamlit for rapid web app development.
- Powered by OpenAI’s Realtime API for advanced text analysis.
- Inspired by concepts of BCI and wellness tracking, though data is simulated for demo purposes.