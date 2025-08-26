import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import networkx as nx
from openai import OpenAI
import json
import warnings
import time
warnings.filterwarnings('ignore')

if "theme" not in st.session_state:
    st.session_state["theme"] = "plotly" 
# OpenAI API Key Setup
if 'OPENAI_API_KEY' not in st.secrets:
    st.warning("OpenAI API key not set in secrets. Enter it below.")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
else:
    openai_api_key = st.secrets['OPENAI_API_KEY']

# Initialize OpenAI client
if openai_api_key:
    client = OpenAI(api_key=openai_api_key)
else:
    client = None
    st.error("OpenAI API key required for real-time analysis. Please provide it.")

@st.cache_data
def load_demo_data():
    """Load demonstration data with realistic patterns"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='H')
    data = []
    prev_sleep = 7.0
    for date in dates:
        hour = date.hour
        day_of_week = date.weekday()
        
        # Heart rate with circadian rhythm
        base_hr = 65 + 15 * np.sin(2 * np.pi * hour / 24 + np.pi/2) + np.random.normal(0, 4)
        heart_rate = max(50, min(120, base_hr - 5 if day_of_week >= 5 else base_hr))
        
        # Stress with workday peaks
        stress_level = max(0, min(1, 0.35 + 0.25 * np.sin(2 * np.pi * (hour + 8) / 24) + 0.15 * np.random.random() + (0.2 if day_of_week < 5 else 0)))
        
        # Steps: higher on active days
        steps = int(1200 * hour / 24 + 2500 * np.random.random()) if 7 < hour < 21 else int(300 * np.random.random())
        
        # Sleep reported in morning
        sleep_duration = np.random.normal(7.5, 1) if hour == 7 else 0
        sleep_duration = max(5, min(9, sleep_duration))
        if sleep_duration > 0:
            prev_sleep = sleep_duration
        
        # Mood influenced by metrics
        mood_score = 0.7 - 0.35 * stress_level + 0.15 * (prev_sleep / 8) + 0.1 * (steps / 10000)
        mood_score = max(0, min(1, mood_score + np.random.normal(0, 0.1)))
        
        moods = ['happy', 'calm', 'energetic', 'focused', 'tired', 'anxious', 'sad', 'neutral']
        mood_weights = np.array([mood_score**1.5, mood_score, mood_score*1.2, mood_score*0.8, (1-mood_score)*1.2, (1-mood_score), (1-mood_score)*0.8, 0.5])
        mood_weights /= mood_weights.sum()
        primary_mood = np.random.choice(moods, p=mood_weights)
        
        # Dreams during REM
        dream_symbols, dream_emotions, vividness = [], {}, 0
        if 1 <= hour <= 5 and np.random.random() > 0.5:
            symbols_pool = ['water', 'flying', 'house', 'animals', 'family', 'work', 'nature', 'travel', 'chase', 'falling']
            dream_symbols = np.random.choice(symbols_pool, size=np.random.randint(2, 5), replace=False).tolist()
            dream_emotions = {
                'joy': np.random.beta(3, 3), 'fear': np.random.beta(2, 4), 'calm': np.random.beta(4, 2),
                'sadness': np.random.beta(1, 5), 'anger': np.random.beta(1, 6)
            }
            vividness = np.random.beta(3, 1.5)
        
        data.append({
            'timestamp': date, 'heart_rate': heart_rate, 'stress_level': stress_level,
            'daily_steps': steps, 'sleep_duration': sleep_duration,
            'mood': primary_mood, 'mood_intensity': mood_score,
            'dream_symbols': dream_symbols, 'dream_emotions': dream_emotions, 'dream_vividness': vividness
        })
    
    df = pd.DataFrame(data)
    df['daily_steps'] = df.groupby(df['timestamp'].dt.date)['daily_steps'].cumsum()
    return df

def analyze_mood_with_openai(text):
    """Use OpenAI Realtime API for real-time mood/emotion analysis"""
    if not client:
        return {"error": "OpenAI client not initialized. Provide API key."}
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in emotional analysis. Analyze the user's input for emotions (e.g., joy, fear, sadness, anger, calm) and estimate intensity (0-1). Return a JSON with primary_mood, intensity, and full_emotions dictionary."},
                {"role": "user", "content": f"Analyze this text for emotions: '{text}'"}
            ],
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"error": f"OpenAI API error: {str(e)}"}

def create_mood_timeline(df):
    """Create mood timeline with enhanced visuals"""
    df_plot = df.copy()
    df_plot['date'] = df_plot['timestamp'].dt.date
    
    mood_colors = {
        'happy': '#FFD700', 'calm': '#87CEEB', 'energetic': '#FF6347',
        'focused': '#9370DB', 'tired': '#A9A9A9', 'anxious': '#FF4500',
        'sad': '#4169E1', 'neutral': '#C0C0C0'
    }
    
    fig = go.Figure()
    for mood, color in mood_colors.items():
        mood_data = df_plot[df_plot['mood'] == mood]
        if not mood_data.empty:
            fig.add_trace(go.Scatter(
                x=mood_data['timestamp'], y=mood_data['mood_intensity'],
                mode='markers+lines', name=mood.title(),
                marker=dict(color=color, size=10, opacity=0.8),
                line=dict(color=color, width=1),
                hovertemplate='<b>%{text}</b><br>Time: %{x}<br>Intensity: %{y:.2f}',
                text=[mood.title()] * len(mood_data)
            ))
    
    fig.update_layout(
        title='Mood Timeline - Past 30 Days',
        xaxis_title='Time', yaxis_title='Mood Intensity (0-1)',
        hovermode='x unified', height=500,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        template='plotly_dark' if st.session_state.get('theme', 'light') == 'dark' else 'plotly_white'
    )
    return fig

def create_health_dashboard(df):
    """Create health metrics dashboard"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Heart Rate', 'Stress Levels', 'Daily Steps', 'Sleep Duration')
    )
    
    df['hr_smooth'] = df['heart_rate'].rolling(window=3).mean()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['hr_smooth'], name='Heart Rate (Smoothed)', line=dict(color='red')), row=1, col=1)
    
    df['stress_smooth'] = df['stress_level'].rolling(window=3).mean()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['stress_smooth'], name='Stress Level', line=dict(color='orange')), row=1, col=2)
    
    daily_steps = df.groupby(df['timestamp'].dt.date)['daily_steps'].max().reset_index(name='steps')
    fig.add_trace(go.Bar(x=daily_steps['timestamp'], y=daily_steps['steps'], name='Daily Steps', marker_color='green'), row=2, col=1)
    
    sleep_data = df[df['sleep_duration'] > 0]
    if not sleep_data.empty:
        fig.add_trace(go.Scatter(x=sleep_data['timestamp'], y=sleep_data['sleep_duration'], mode='markers+lines', marker=dict(color='purple')), row=2, col=2)
    
    fig.update_layout(height=600, showlegend=False, title_text="Health Metrics Dashboard", template=st.session_state.get('theme', 'light'))
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="BPM", row=1, col=1)
    fig.update_yaxes(title_text="Stress (0-1)", row=1, col=2)
    fig.update_yaxes(title_text="Steps", row=2, col=1)
    fig.update_yaxes(title_text="Hours", row=2, col=2)
    return fig

def create_dream_analysis(df):
    """Create dream analysis visualizations"""
    dream_data = df[df['dream_vividness'] > 0].copy()
    
    if dream_data.empty:
        return None, None, "No dream data available for analysis."
    
    all_symbols = [sym for symbols in dream_data['dream_symbols'] for sym in symbols]
    symbol_counts = pd.Series(all_symbols).value_counts()
    fig_symbols = px.pie(names=symbol_counts.index, values=symbol_counts.values, title="Dream Symbols Distribution", hole=0.3)
    fig_symbols.update_layout(height=400)
    
    emotion_data = []
    for emotions in dream_data['dream_emotions']:
        if emotions:
            emotion_data.extend([(k, v) for k, v in emotions.items()])
    
    if emotion_data:
        emotion_df = pd.DataFrame(emotion_data, columns=['emotion', 'intensity'])
        fig_emotions = px.histogram(emotion_df, x='emotion', y='intensity', title="Dream Emotion Intensities", histfunc='avg')
        fig_emotions.update_layout(height=400)
    else:
        fig_emotions = None
    
    latest_dream = dream_data.iloc[-1] if not dream_data.empty else None
    dream_insight = "No recent dreams to analyze."
    if latest_dream is not None and client:
        try:
            symbols = ", ".join(latest_dream['dream_symbols'])
            emotions = ", ".join([f"{k}: {v:.2f}" for k, v in latest_dream['dream_emotions'].items()])
            prompt = f"Interpret this dream: Symbols: {symbols}. Emotions: {emotions}. Vividness: {latest_dream['dream_vividness']:.2f}."
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a dream interpretation expert. Provide a brief, meaningful interpretation of the dream based on symbols, emotions, and vividness."},
                    {"role": "user", "content": prompt}
                ]
            )
            dream_insight = response.choices[0].message.content
        except Exception as e:
            dream_insight = f"Error in dream analysis: {str(e)}"
    
    return fig_symbols, fig_emotions, dream_insight

def simulate_real_time_data():
    """Simulate real-time data based on current time"""
    current_time = datetime.datetime.now()
    hour = current_time.hour
    
    heart_rate = max(50, min(120, 65 + 15 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 4)))
    stress_level = max(0, min(1, 0.35 + 0.25 * np.sin(2 * np.pi * (hour + 8) / 24) + 0.15 * np.random.random()))
    steps = int(800 * hour / 24 + 1500 * np.random.random()) if 7 < hour < 21 else int(300 * np.random.random())
    
    moods = ['happy', 'calm', 'energetic', 'focused', 'tired', 'anxious', 'neutral']
    mood_weights = [0.25, 0.2, 0.15, 0.1, 0.1, 0.1, 0.1]
    current_mood = np.random.choice(moods, p=np.array(mood_weights) / sum(mood_weights))
    mood_intensity = np.random.beta(4, 2)
    
    return {
        'heart_rate': heart_rate, 'stress_level': stress_level, 'daily_steps': steps,
        'current_mood': current_mood, 'mood_intensity': mood_intensity, 'timestamp': current_time
    }

def show_dashboard(df):
    """Show main dashboard with real-time analysis"""
    st.header("🏠 Dashboard Overview")
    
    current_data = simulate_real_time_data()
    
    cols = st.columns(4)
    with cols[0]:
        st.markdown('<div class="metric-card"><h3>BCI Status</h3><div><span class="status-indicator status-active"></span>Active</div><p>1024 electrodes</p></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="metric-card"><h3>Current Mood</h3><div style="font-size: 24px;">{current_data["current_mood"].title()}</div><p>Intensity: {current_data["mood_intensity"]:.2f}</p></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="metric-card"><h3>Heart Rate</h3><div style="font-size: 24px; color: red;">{current_data["heart_rate"]:.0f} BPM</div><p>Normal range</p></div>', unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f'<div class="metric-card"><h3>Stress Level</h3><div style="font-size: 24px; color: orange;">{current_data["stress_level"]:.2f}</div><p>{"Low" if current_data["stress_level"] < 0.4 else "Moderate" if current_data["stress_level"] < 0.7 else "High"}</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Mood Timeline (Last 7 Days)")
        recent_df = df[df['timestamp'] >= df['timestamp'].max() - pd.Timedelta(days=7)]
        mood_fig = create_mood_timeline(recent_df)
        st.plotly_chart(mood_fig, use_container_width=True)
    
    with col2:
        st.subheader("💤 Sleep & Dream Activity")
        sleep_df = df[df['sleep_duration'] > 0].tail(7)
        if not sleep_df.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=sleep_df['timestamp'].dt.date, y=sleep_df['sleep_duration'], name='Sleep', marker_color='lightblue'))
            dream_nights = sleep_df[sleep_df['dream_vividness'] > 0]
            if not dream_nights.empty:
                fig.add_trace(go.Scatter(x=dream_nights['timestamp'].dt.date, y=dream_nights['dream_vividness'] * max(sleep_df['sleep_duration']), mode='markers', name='Dreams', marker=dict(color='purple', size=12), yaxis='y2'))
            fig.update_layout(xaxis_title='Date', yaxis_title='Hours', yaxis2=dict(overlaying='y', side='right', title='Vividness'), height=400, template=st.session_state['theme'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No recent sleep data")
    
    st.markdown("---")
    st.subheader("🧠 Real-Time Mood Analysis from User Input")
    user_text = st.text_area("Describe your current mood, dream, or journal entry for AI analysis:")
    if st.button("Analyze with OpenAI") and user_text:
        with st.spinner("Analyzing with OpenAI Realtime API..."):
            result = analyze_mood_with_openai(user_text)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"Detected Primary Mood: {result['primary_mood'].title()} (Intensity: {result['intensity']:.2f})")
                st.json(result['full_emotions'])
    
    with st.expander("🔍 Quick Insights"):
        cols = st.columns(2)
        with cols[0]:
            st.info("🧠 Mood improves with activity")
            st.success("✅ Sleep quality up")
        with cols[1]:
            st.warning("⚠️ Afternoon stress high")
            st.info("💡 Try meditation")
    
    if st.button("📥 Download Data"):
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "dream_data.csv", "text/csv")

def show_real_time_monitoring():
    """Show real-time monitoring page"""
    st.header("🧠 Real-Time Neural Monitoring")
    
    auto_refresh = st.checkbox("Auto-refresh (every 5s)", value=True)
    
    if 'last_update' not in st.session_state:
        st.session_state['last_update'] = time.time()
    
    if auto_refresh and time.time() - st.session_state['last_update'] > 5:
        st.session_state['last_update'] = time.time()
        st.experimental_rerun()
    
    current_data = simulate_real_time_data()
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f'<div class="metric-card"><h3>Neural Activity</h3><div><span class="status-indicator status-active"></span>Active</div><p>Alpha waves dominant</p></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="metric-card"><h3>Heart Rate</h3><div style="font-size: 24px; color: red;">{current_data["heart_rate"]:.0f} BPM</div></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="metric-card"><h3>Stress</h3><div style="font-size: 24px; color: orange;">{current_data["stress_level"]:.2f}</div></div>', unsafe_allow_html=True)
    
    st.subheader("📡 Brain Wave Patterns")
    t = np.linspace(0, 10, 1000)
    alpha = np.sin(2 * np.pi * 10 * t) * np.random.normal(1, 0.1, 1000)
    beta = np.sin(2 * np.pi * 20 * t) * np.random.normal(0.8, 0.1, 1000)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=alpha, name='Alpha (8-12 Hz)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=t, y=beta, name='Beta (12-30 Hz)', line=dict(color='green')))
    fig.update_layout(title='Simulated EEG Waves', xaxis_title='Time (s)', yaxis_title='Amplitude', height=400, template=st.session_state['theme'])
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🧠 Neural Network")
    G = nx.Graph()
    regions = ['Frontal', 'Temporal', 'Parietal', 'Occipital']
    for i, region in enumerate(regions):
        G.add_node(region)
        for j in range(i + 1, len(regions)):
            if np.random.random() > 0.5:
                G.add_edge(regions[i], regions[j])
    
    pos = nx.spring_layout(G)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    node_x, node_y = zip(*[pos[node] for node in G.nodes()])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=2, color='gray'), hoverinfo='none'))
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=list(G.nodes()), textposition="bottom center", marker=dict(size=20, color='lightblue')))
    fig.update_layout(title='Neural Connections', showlegend=False, height=400, template=st.session_state['theme'])
    st.plotly_chart(fig, use_container_width=True)

def show_health_analytics(df):
    """Show health analytics page"""
    st.header("📊 Health Analytics")
    
    metrics = st.multiselect("Select Metrics", ['heart_rate', 'stress_level', 'daily_steps', 'sleep_duration', 'mood_intensity'], default=['heart_rate', 'stress_level'])
    
    if metrics:
        fig = go.Figure()
        for metric in metrics:
            if metric == 'daily_steps':
                daily_data = df.groupby(df['timestamp'].dt.date)[metric].max().reset_index()
                fig.add_trace(go.Bar(x=daily_data['timestamp'], y=daily_data[metric], name=metric.replace('_', ' ').title()))
            else:
                fig.add_trace(go.Scatter(x=df['timestamp'], y=df[metric], name=metric.replace('_', ' ').title()))
        fig.update_layout(title='Health Metrics Over Time', xaxis_title='Time', yaxis_title='Value', height=500, template=st.session_state['theme'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🔗 Correlations")
    corr = df[['heart_rate', 'stress_level', 'daily_steps', 'sleep_duration', 'mood_intensity']].corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r')
    fig.update_layout(title='Metric Correlations', height=400, template=st.session_state['theme'])
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📝 Insights")
    if corr.loc['stress_level', 'mood_intensity'] < -0.3:
        st.warning("High stress linked to lower mood. Consider relaxation techniques.")
    if corr.loc['sleep_duration', 'mood_intensity'] > 0.3:
        st.success("Good sleep correlates with better mood!")

def show_dream_analysis(df):
    """Show dream analysis page"""
    st.header("🌙 Dream Analysis")
    
    fig_symbols, fig_emotions, dream_insight = create_dream_analysis(df)
    
    st.subheader("📊 Dream Statistics")
    dream_data = df[df['dream_vividness'] > 0]
    st.write(f"Total Dreams: {len(dream_data)}")
    st.write(f"Average Vividness: {dream_data['dream_vividness'].mean():.2f}" if not dream_data.empty else "No dream data")
    
    if fig_symbols:
        st.subheader("🔮 Dream Symbols")
        st.plotly_chart(fig_symbols, use_container_width=True)
    
    if fig_emotions:
        st.subheader("😊 Dream Emotions")
        st.plotly_chart(fig_emotions, use_container_width=True)
    
    st.subheader("🧠 Latest Dream Interpretation")
    st.write(dream_insight)

def show_ai_companion():
    """Show AI companion page with OpenAI integration"""
    st.header("🤖 AI Companion")
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    current_data = simulate_real_time_data()
    context = f"Current mood: {current_data['current_mood']} (intensity: {current_data['mood_intensity']:.2f}). Stress: {current_data['stress_level']:.2f}."
    
    user_input = st.text_input("Talk to your AI Companion:", key="chat_input")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Breathing Exercise"):
            st.session_state['chat_history'].append(("AI", "Let's do a 4-7-8 breathing exercise: Inhale for 4 seconds, hold for 7, exhale for 8. Repeat 4 times."))
    with col2:
        if st.button("Quick Meditation"):
            st.session_state['chat_history'].append(("AI", "Find a quiet space. Focus on your breath for 2 minutes, letting thoughts pass without judgment."))
    with col3:
        if st.button("Mood Check"):
            st.session_state['chat_history'].append(("AI", f"Based on simulated data, your current mood is {current_data['current_mood']} with intensity {current_data['mood_intensity']:.2f}. How do you feel?"))
    
    if user_input:
        st.session_state['chat_history'].append(("You", user_input))
        if client:
            try:
                result = analyze_mood_with_openai(user_input)
                if "error" in result:
                    response = f"Error: {result['error']}"
                else:
                    primary_mood = result['primary_mood']
                    intensity = result['intensity']
                    response = f"I sense {primary_mood} (intensity: {intensity:.2f}) in your words. {context} How can I assist you further?"
                    if intensity > 0.7 and primary_mood in ['anxious', 'sad']:
                        response += " Would you like a calming exercise?"
            except Exception as e:
                response = f"Error processing response: {str(e)}"
        else:
            response = "OpenAI API key required for real-time analysis."
        st.session_state['chat_history'].append(("AI", response))
    
    st.subheader("💬 Chat History")
    for sender, message in st.session_state['chat_history'][-10:]:
        if sender == "You":
            st.markdown(f'<div class="chat-message user-message"><b>You:</b> {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message ai-message"><b>AI:</b> {message}</div>', unsafe_allow_html=True)

def show_settings():
    """Show settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("BCI Configuration")
    electrode_count = st.slider("Number of Electrodes", 128, 2048, 1024, step=128)
    st.write(f"Simulated electrodes: {electrode_count}")
    
    st.subheader("Health Alerts")
    heart_rate_alert = st.number_input("Heart Rate Alert Threshold (BPM)", 50, 150, 100)
    stress_alert = st.number_input("Stress Alert Threshold (0-1)", 0.0, 1.0, 0.8, step=0.1)
    
    st.subheader("Theme")
    theme = st.selectbox("Choose Theme", ["Light", "Dark"], index=0 if st.session_state.get('theme', 'light') == 'light' else 1)
    st.session_state['theme'] = theme.lower()
    
    if st.button("Save Settings"):
        st.session_state['settings'] = {
            'electrode_count': electrode_count,
            'heart_rate_alert': heart_rate_alert,
            'stress_alert': stress_alert
        }
        st.success("Settings saved!")

# App Config
st.set_page_config(page_title="Neural Dream Weaver", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# Enhanced CSS
st.markdown("""
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .main { background: linear-gradient(to bottom, #f0f4f8, #d9e2ec); }
    [data-theme="dark"] .main { background: linear-gradient(to bottom, #1e1e1e, #2c3e50); color: white; }
    .main-header { text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 2rem; animation: fadeIn 1s ease-in; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .metric-card { background: white; padding: 1.2rem; border-radius: 12px; box-shadow: 0 3px 6px rgba(0,0,0,0.15); text-align: center; transition: transform 0.3s; }
    .metric-card:hover { transform: translateY(-5px); }
    [data-theme="dark"] .metric-card { background: #333; color: white; }
    .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 6px; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { transform: scale(0.95); } 70% { transform: scale(1.05); } 100% { transform: scale(0.95); } }
    .status-active { background-color: #4CAF50; }
    .status-warning { background-color: #FF9800; }
    .status-inactive { background-color: #F44336; }
    .chat-message { padding: 12px; margin: 8px 0; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); transition: all 0.3s; }
    .chat-message:hover { box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
    .user-message { background-color: #E3F2FD; text-align: right; }
    .ai-message { background-color: #F1F8E9; text-align: left; }
    [data-theme="dark"] .user-message { background-color: #2C3E50; }
    [data-theme="dark"] .ai-message { background-color: #34495E; }
    .stButton > button { border-radius: 8px; transition: background 0.3s; }
    .stButton > button:hover { background: #5A67D8; color: white; }
</style>
""", unsafe_allow_html=True)

def main():
    """Main app function"""
    st.markdown('<div class="main-header"><h1>🧠🌙 Neural Dream Weaver</h1><p>Advanced BCI Dream Analysis & Mood Synchronization with OpenAI</p></div>', unsafe_allow_html=True)
    
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a section:", ["🏠 Dashboard", "🧠 Real-Time Monitoring", "📊 Health Analytics", "🌙 Dream Analysis", "🤖 AI Companion", "⚙️ Settings"])
    
    df = load_demo_data()
    
    if page == "🏠 Dashboard":
        show_dashboard(df)
    elif page == "🧠 Real-Time Monitoring":
        show_real_time_monitoring()
    elif page == "📊 Health Analytics":
        show_health_analytics(df)
    elif page == "🌙 Dream Analysis":
        show_dream_analysis(df)
    elif page == "🤖 AI Companion":
        show_ai_companion()
    elif page == "⚙️ Settings":
        show_settings()

if __name__ == "__main__":
    main()