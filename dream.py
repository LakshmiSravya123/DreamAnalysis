import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#from plotly.graph_objects import make_subplots
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import time

# Import our NDW system (in production, this would be: from ndw_core import *)
# For demo purposes, we'll include simplified versions

@st.cache_data
def load_demo_data():
    """Load demo dream data"""
    demo_dreams = [
        {
            "id": "dream_001",
            "date": "2024-08-15",
            "symbols": ["flying", "water", "mountains"],
            "emotions": {"freedom": 0.8, "peace": 0.7, "wonder": 0.9},
            "sleep_stage": "REM",
            "duration": 12.5,
            "confidence": 0.87,
            "insights": [
                "Strong desire for personal freedom and transcendence",
                "Connection to natural elements suggests grounding needs",
                "High creativity indicators in theta patterns"
            ]
        },
        {
            "id": "dream_002", 
            "date": "2024-08-16",
            "symbols": ["falling", "darkness", "doors"],
            "emotions": {"anxiety": 0.9, "confusion": 0.6, "curiosity": 0.4},
            "sleep_stage": "NREM",
            "duration": 8.3,
            "confidence": 0.73,
            "insights": [
                "Processing of control-related anxieties",
                "Threshold symbolism indicates life transitions",
                "Elevated stress markers in beta frequencies"
            ]
        },
        {
            "id": "dream_003",
            "date": "2024-08-17", 
            "symbols": ["animals", "family", "childhood_home"],
            "emotions": {"nostalgia": 0.8, "love": 0.9, "protection": 0.7},
            "sleep_stage": "REM",
            "duration": 15.2,
            "confidence": 0.91,
            "insights": [
                "Deep memory consolidation with family bonds",
                "Instinctual protection mechanisms activated",
                "Strong gamma coherence suggesting memory integration"
            ]
        }
    ]
    return demo_dreams

def create_neural_waveform():
    """Generate realistic-looking EEG waveform"""
    t = np.linspace(0, 10, 1000)
    
    # Mix different frequency bands
    delta = 2 * np.sin(2 * np.pi * 2 * t) * np.random.normal(1, 0.1, 1000)
    theta = 1.5 * np.sin(2 * np.pi * 6 * t) * np.random.normal(1, 0.1, 1000) 
    alpha = 1 * np.sin(2 * np.pi * 10 * t) * np.random.normal(1, 0.1, 1000)
    beta = 0.5 * np.sin(2 * np.pi * 20 * t) * np.random.normal(1, 0.1, 1000)
    
    signal = delta + theta + alpha + beta + np.random.normal(0, 0.2, 1000)
    
    return t, signal

def create_frequency_analysis():
    """Create frequency domain analysis"""
    frequencies = np.array([1, 2, 3, 4, 6, 8, 10, 12, 15, 20, 25, 30, 40])
    power = np.array([0.8, 0.9, 0.7, 0.6, 0.8, 0.5, 0.7, 0.4, 0.3, 0.5, 0.2, 0.1, 0.15])
    bands = ['Delta', 'Delta', 'Delta', 'Delta', 'Theta', 'Theta', 'Alpha', 'Alpha', 'Beta', 'Beta', 'Beta', 'Gamma', 'Gamma']
    
    return frequencies, power, bands

# Streamlit App Configuration
st.set_page_config(
    page_title="Neural Dream Workshop",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .dream-card {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .insight-box {
        background: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; text-align: center; margin-bottom: 0;">🧠 Neural Dream Workshop</h1>
        <p style="color: white; text-align: center; font-size: 1.2em; margin-top: 0;">
            AI-Powered Dream Analysis & Enhancement System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.title("🎛️ NDW Control Panel")
    
    mode = st.sidebar.selectbox(
        "Select Mode",
        ["🔴 Live Dream Capture", "📊 Dream Analysis", "📈 Progress Tracking", "⚡ Enhancement Protocols", "ℹ️ About NDW"]
    )
    
    # Load demo data
    demo_dreams = load_demo_data()
    
    if mode == "🔴 Live Dream Capture":
        live_capture_mode(demo_dreams)
    elif mode == "📊 Dream Analysis":
        analysis_mode(demo_dreams)
    elif mode == "📈 Progress Tracking":
        progress_tracking_mode(demo_dreams)
    elif mode == "⚡ Enhancement Protocols":
        enhancement_mode(demo_dreams)
    else:
        about_mode()

def live_capture_mode(demo_dreams):
    st.header("🔴 Live Dream Capture Session")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🧠 Neural Signal Monitoring")
        
        # Real-time neural waveform simulation
        if st.button("▶️ Start Dream Capture", type="primary"):
            # Create placeholder for live updates
            chart_placeholder = st.empty()
            status_placeholder = st.empty()
            
            with st.spinner("🛌 Waiting for sleep onset..."):
                time.sleep(2)
                
            status_placeholder.success("✅ REM sleep detected - capturing dreams...")
            
            # Simulate real-time data
            for i in range(10):
                t, signal = create_neural_waveform()
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=t, y=signal,
                    mode='lines',
                    name='Neural Activity',
                    line=dict(color='#667eea', width=1.5)
                ))
                
                fig.update_layout(
                    title="Real-time Neural Signals (Channel 1)",
                    xaxis_title="Time (seconds)",
                    yaxis_title="Amplitude (μV)",
                    height=400,
                    showlegend=False
                )
                
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                time.sleep(0.5)
            
            status_placeholder.success("🎯 Dream capture complete! Processing analysis...")
            
            # Show capture results
            st.success("✨ **Dream Successfully Captured!**")
            
            # Display captured dream summary
            st.markdown("""
            <div class="dream-card">
                <h4>🆔 Dream Session: dream_live_001</h4>
                <p><strong>Duration:</strong> 14.2 minutes</p>
                <p><strong>Sleep Stage:</strong> REM (High Activity)</p>
                <p><strong>Detected Elements:</strong> Flying, Ocean, Golden Light</p>
                <p><strong>Emotional Tone:</strong> Freedom (0.85), Wonder (0.78), Joy (0.72)</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("⚙️ Capture Settings")
        
        duration = st.slider("Capture Duration (minutes)", 5, 60, 15)
        sensitivity = st.slider("Neural Sensitivity", 0.1, 1.0, 0.7)
        
        st.subheader("🎯 Current Status")
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #667eea;">READY</h3>
            <p>Neuralink Interface Connected</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("📊 Quick Stats")
        st.metric("Sessions Today", "3", "↑ 2")
        st.metric("Avg Dream Quality", "87%", "↑ 5%")
        st.metric("Enhancement Score", "92%", "↑ 8%")

def analysis_mode(demo_dreams):
    st.header("📊 Dream Analysis Dashboard")
    
    # Dream selector
    dream_options = {f"Dream {i+1} ({dream['date']})": dream for i, dream in enumerate(demo_dreams)}
    selected_dream_key = st.selectbox("Select Dream to Analyze", list(dream_options.keys()))
    selected_dream = dream_options[selected_dream_key]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Confidence Score", 
            f"{selected_dream['confidence']:.0%}",
            delta=f"{(selected_dream['confidence'] - 0.75):.0%}"
        )
    
    with col2:
        st.metric(
            "Dream Duration",
            f"{selected_dream['duration']:.1f} min",
            delta="Normal range"
        )
    
    with col3:
        st.metric(
            "Sleep Stage",
            selected_dream['sleep_stage'],
            delta="Optimal" if selected_dream['sleep_stage'] == "REM" else "Good"
        )
    
    # Detailed Analysis Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Visual Analysis", "🔮 Symbolism", "😊 Emotions", "🧠 Neural Data"])
    
    with tab1:
        st.subheader("Dream Visualization")
        
        # Create dream symbol visualization
        symbols = selected_dream['symbols']
        symbol_data = pd.DataFrame({
            'Symbol': symbols,
            'Intensity': np.random.uniform(0.3, 1.0, len(symbols)),
            'Frequency': np.random.randint(1, 5, len(symbols)),
            'Category': ['Nature', 'Motion', 'Emotion'][:len(symbols)]
        })
        
        # Symbol intensity chart
        fig_symbols = px.bar(
            symbol_data, 
            x='Symbol', 
            y='Intensity',
            color='Category',
            title="Dream Symbol Analysis",
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
        )
        fig_symbols.update_layout(height=400)
        st.plotly_chart(fig_symbols, use_container_width=True)
        
        # Neural frequency analysis
        freqs, power, bands = create_frequency_analysis()
        
        fig_freq = go.Figure()
        colors = {'Delta': '#1f77b4', 'Theta': '#ff7f0e', 'Alpha': '#2ca02c', 'Beta': '#d62728', 'Gamma': '#9467bd'}
        
        for band in set(bands):
            mask = np.array(bands) == band
            fig_freq.add_trace(go.Scatter(
                x=freqs[mask],
                y=power[mask],
                mode='lines+markers',
                name=f'{band} Band',
                line=dict(color=colors[band], width=3),
                marker=dict(size=8)
            ))
        
        fig_freq.update_layout(
            title="Brainwave Frequency Analysis During Dream",
            xaxis_title="Frequency (Hz)",
            yaxis_title="Power Spectral Density",
            height=400
        )
        st.plotly_chart(fig_freq, use_container_width=True)
    
    with tab2:
        st.subheader("🔮 Symbolic Interpretation")
        
        # Symbol meanings database
        symbol_meanings = {
            "flying": {
                "primary": "Freedom and transcendence",
                "secondary": "Desire to escape limitations",
                "psychological": "Seeking personal empowerment",
                "cultural": "Universal symbol of aspiration",
                "therapeutic": "Explore areas of constraint in waking life"
            },
            "water": {
                "primary": "Emotional state and unconscious mind", 
                "secondary": "Cleansing and renewal",
                "psychological": "Processing emotional experiences",
                "cultural": "Life force across all cultures",
                "therapeutic": "Engage in emotional expression practices"
            },
            "mountains": {
                "primary": "Challenges and spiritual growth",
                "secondary": "Stability and permanence", 
                "psychological": "Overcoming obstacles",
                "cultural": "Sacred spaces in many traditions",
                "therapeutic": "Set achievable goals for personal growth"
            },
            "falling": {
                "primary": "Loss of control or security",
                "secondary": "Fear of failure",
                "psychological": "Anxiety about life changes",
                "cultural": "Common across all human cultures",
                "therapeutic": "Practice grounding and security techniques"
            },
            "darkness": {
                "primary": "Unknown or unconscious aspects",
                "secondary": "Fear of the hidden",
                "psychological": "Shadow work and integration",
                "cultural": "Mystery and potential",
                "therapeutic": "Explore hidden aspects of personality"
            },
            "doors": {
                "primary": "Opportunities and transitions",
                "secondary": "Choices and pathways",
                "psychological": "Life transitions and decisions",
                "cultural": "Thresholds between worlds",
                "therapeutic": "Consider current life choices"
            },
            "animals": {
                "primary": "Instinctual nature and drives",
                "secondary": "Connection to natural self",
                "psychological": "Primal energies and desires",
                "cultural": "Spirit guides and totems",
                "therapeutic": "Connect with natural instincts"
            },
            "family": {
                "primary": "Core relationships and bonds",
                "secondary": "Security and belonging",
                "psychological": "Attachment and identity formation",
                "cultural": "Foundation of social structure",
                "therapeutic": "Strengthen important relationships"
            },
            "childhood_home": {
                "primary": "Foundation and origins",
                "secondary": "Safety and familiarity",
                "psychological": "Core identity and values",
                "cultural": "Ancestral connections",
                "therapeutic": "Reflect on formative experiences"
            }
        }
        
        for symbol in selected_dream['symbols']:
            if symbol in symbol_meanings:
                meaning = symbol_meanings[symbol]
                
                st.markdown(f"""
                <div class="dream-card">
                    <h4>🎭 {symbol.title()}</h4>
                    <p><strong>Primary Meaning:</strong> {meaning['primary']}</p>
                    <p><strong>Psychological Aspect:</strong> {meaning['psychological']}</p>
                    <p><strong>Cultural Context:</strong> {meaning['cultural']}</p>
                    <p><strong>💡 Therapeutic Suggestion:</strong> {meaning['therapeutic']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("😊 Emotional Landscape")
        
        # Emotion radar chart
        emotions = list(selected_dream['emotions'].keys())
        values = list(selected_dream['emotions'].values())
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the polygon
            theta=emotions + [emotions[0]],
            fill='toself',
            name='Emotional Profile',
            line_color='#667eea',
            fillcolor='rgba(102, 126, 234, 0.3)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False,
            title="Emotional Analysis Radar",
            height=500
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Emotion timeline
        st.subheader("🌊 Emotional Flow During Dream")
        
        # Simulate emotion changes over time
        time_points = np.linspace(0, selected_dream['duration'], 20)
        emotion_timeline = {}
        
        for emotion, base_value in selected_dream['emotions'].items():
            # Add some variation over time
            variation = np.random.normal(0, 0.1, len(time_points))
            emotion_timeline[emotion] = np.clip(base_value + variation, 0, 1)
        
        fig_timeline = go.Figure()
        
        colors = ['#667eea', '#764ba2', '#f093fb', '#48cae4', '#f72585']
        for i, (emotion, values) in enumerate(emotion_timeline.items()):
            fig_timeline.add_trace(go.Scatter(
                x=time_points,
                y=values,
                mode='lines+markers',
                name=emotion.title(),
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=6)
            ))
        
        fig_timeline.update_layout(
            title="Emotional Intensity Over Dream Duration",
            xaxis_title="Time (minutes)",
            yaxis_title="Emotional Intensity",
            height=400,
            yaxis=dict(range=[0, 1])
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with tab4:
        st.subheader("🧠 Neural Signal Analysis")
        
        # Raw neural signal
        t, signal = create_neural_waveform()
        
        fig_neural = go.Figure()
        fig_neural.add_trace(go.Scatter(
            x=t,
            y=signal,
            mode='lines',
            name='Neural Activity',
            line=dict(color='#667eea', width=1)
        ))
        
        fig_neural.update_layout(
            title="Raw Neural Signal (Sample Channel)",
            xaxis_title="Time (seconds)",
            yaxis_title="Amplitude (μV)",
            height=300
        )
        st.plotly_chart(fig_neural, use_container_width=True)
        
        # Frequency bands breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-box">
                <h4>🌊 Delta Waves (1-4 Hz)</h4>
                <p><strong>Power:</strong> 68% of total</p>
                <p><strong>Significance:</strong> Deep sleep maintenance</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-box">
                <h4>🎯 Theta Waves (4-8 Hz)</h4>
                <p><strong>Power:</strong> 45% of total</p>
                <p><strong>Significance:</strong> Dream generation and creativity</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
                <h4>⚡ Alpha Waves (8-12 Hz)</h4>
                <p><strong>Power:</strong> 32% of total</p>
                <p><strong>Significance:</strong> Relaxed awareness</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-box">
                <h4>🔥 Gamma Waves (30+ Hz)</h4>
                <p><strong>Power:</strong> 15% of total</p>
                <p><strong>Significance:</strong> Memory consolidation</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Insights Section
    st.subheader("💡 AI-Generated Insights")
    
    for i, insight in enumerate(selected_dream['insights']):
        st.markdown(f"""
        <div class="insight-box">
            <p><strong>Insight {i+1}:</strong> {insight}</p>
        </div>
        """, unsafe_allow_html=True)

def progress_tracking_mode(demo_dreams):
    st.header("📈 Progress Tracking & Analytics")
    
    # Generate historical data
    dates = pd.date_range(start='2024-07-01', end='2024-08-19', freq='D')
    
    # Simulate metrics over time
    dream_quality = 0.6 + 0.3 * np.sin(np.linspace(0, 4*np.pi, len(dates))) + np.random.normal(0, 0.05, len(dates))
    sleep_efficiency = 0.7 + 0.2 * np.cos(np.linspace(0, 3*np.pi, len(dates))) + np.random.normal(0, 0.03, len(dates))
    emotional_balance = 0.65 + 0.25 * np.sin(np.linspace(0, 2*np.pi, len(dates))) + np.random.normal(0, 0.04, len(dates))
    
    # Clip values to realistic ranges
    dream_quality = np.clip(dream_quality, 0, 1)
    sleep_efficiency = np.clip(sleep_efficiency, 0, 1)
    emotional_balance = np.clip(emotional_balance, 0, 1)
    
    progress_df = pd.DataFrame({
        'Date': dates,
        'Dream Quality': dream_quality,
        'Sleep Efficiency': sleep_efficiency,
        'Emotional Balance': emotional_balance
    })
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_quality = dream_quality[-1]
        prev_quality = dream_quality[-8]  # Week ago
        delta_quality = current_quality - prev_quality
        
        st.metric(
            "Dream Quality Score",
            f"{current_quality:.1%}",
            delta=f"{delta_quality:+.1%}"
        )
    
    with col2:
        total_dreams = len(demo_dreams) + 15  # Add some historical
        st.metric(
            "Total Dreams Analyzed",
            f"{total_dreams}",
            delta="↑ 3 this week"
        )
    
    with col3:
        avg_duration = np.mean([dream['duration'] for dream in demo_dreams])
        st.metric(
            "Average Dream Duration",
            f"{avg_duration:.1f} min",
            delta="↑ 2.1 min"
        )
    
    with col4:
        enhancement_score = np.random.uniform(0.85, 0.95)
        st.metric(
            "Enhancement Effectiveness",
            f"{enhancement_score:.0%}",
            delta="↑ 8%"
        )
    
    # Progress Charts
    tab1, tab2, tab3 = st.tabs(["📊 Overall Progress", "🎯 Dream Patterns", "🔄 Enhancement History"])
    
    with tab1:
        st.subheader("Progress Over Time")
        
        fig_progress = go.Figure()
        
        fig_progress.add_trace(go.Scatter(
            x=progress_df['Date'],
            y=progress_df['Dream Quality'],
            mode='lines+markers',
            name='Dream Quality',
            line=dict(color='#667eea', width=3)
        ))
        
        fig_progress.add_trace(go.Scatter(
            x=progress_df['Date'],
            y=progress_df['Sleep Efficiency'],
            mode='lines+markers',
            name='Sleep Efficiency',
            line=dict(color='#764ba2', width=3)
        ))
        
        fig_progress.add_trace(go.Scatter(
            x=progress_df['Date'],
            y=progress_df['Emotional Balance'],
            mode='lines+markers',
            name='Emotional Balance',
            line=dict(color='#f093fb', width=3)
        ))
        
        fig_progress.update_layout(
            title="30-Day Progress Overview",
            xaxis_title="Date",
            yaxis_title="Score (0-1)",
            height=500,
            yaxis=dict(range=[0, 1])
        )
        st.plotly_chart(fig_progress, use_container_width=True)
        
        # Weekly summary
        st.subheader("📋 Weekly Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🎯 This Week's Achievements:**
            - 🏆 Achieved highest dream quality score (91%)
            - 🧠 Completed 3 enhancement sessions
            - 😴 Improved REM sleep duration by 15%
            - 💡 Identified 2 new recurring symbols
            """)
        
        with col2:
            st.markdown("""
            **📈 Areas of Improvement:**
            - 🎨 Increase creative dream elements
            - 😌 Reduce anxiety-related dream content
            - ⏰ Extend average dream duration
            - 🔄 Try new enhancement protocols
            """)
    
    with tab2:
        st.subheader("🎯 Dream Pattern Analysis")
        
        # Symbol frequency analysis
        all_symbols = []
        for dream in demo_dreams:
            all_symbols.extend(dream['symbols'])
        
        symbol_counts = pd.Series(all_symbols).value_counts()
        
        fig_symbols = px.pie(
            values=symbol_counts.values,
            names=symbol_counts.index,
            title="Most Frequent Dream Symbols",
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#48cae4', '#f72585']
        )
        fig_symbols.update_layout(height=400)
        st.plotly_chart(fig_symbols, use_container_width=True)
        
        # Sleep stage distribution
        stages = [dream['sleep_stage'] for dream in demo_dreams]
        stage_counts = pd.Series(stages).value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_stages = px.bar(
                x=stage_counts.index,
                y=stage_counts.values,
                title="Sleep Stage Distribution",
                color=stage_counts.values,
                color_continuous_scale='viridis'
            )
            fig_stages.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_stages, use_container_width=True)
        
        with col2:
            # Emotion trends
            all_emotions = {}
            for dream in demo_dreams:
                for emotion, score in dream['emotions'].items():
                    if emotion not in all_emotions:
                        all_emotions[emotion] = []
                    all_emotions[emotion].append(score)
            
            emotion_avg = {k: np.mean(v) for k, v in all_emotions.items()}
            
            fig_emotions = px.bar(
                x=list(emotion_avg.keys()),
                y=list(emotion_avg.values()),
                title="Average Emotional Intensity",
                color=list(emotion_avg.values()),
                color_continuous_scale='plasma'
            )
            fig_emotions.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_emotions, use_container_width=True)
    
    with tab3:
        st.subheader("🔄 Enhancement Protocol History")
        
        # Generate enhancement history
        enhancement_dates = pd.date_range(start='2024-08-01', end='2024-08-19', freq='2D')
        protocols = ['Alpha Relaxation', 'Theta Creativity', 'Gamma Memory', 'Delta Deep Sleep', 'Lucid Dreaming']
        
        enhancement_history = []
        for date in enhancement_dates:
            protocol = np.random.choice(protocols)
            effectiveness = np.random.uniform(0.7, 0.95)
            duration = np.random.randint(10, 45)
            
            enhancement_history.append({
                'Date': date,
                'Protocol': protocol,
                'Effectiveness': effectiveness,
                'Duration': duration
            })
        
        enhancement_df = pd.DataFrame(enhancement_history)
        
        # Enhancement effectiveness over time
        fig_enhancement = px.scatter(
            enhancement_df,
            x='Date',
            y='Effectiveness',
            color='Protocol',
            size='Duration',
            title="Enhancement Protocol Effectiveness",
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#48cae4', '#f72585']
        )
        fig_enhancement.update_layout(height=400)
        st.plotly_chart(fig_enhancement, use_container_width=True)
        
        # Protocol comparison
        protocol_stats = enhancement_df.groupby('Protocol').agg({
            'Effectiveness': 'mean',
            'Duration': 'mean'
        }).reset_index()
        
        st.subheader("📊 Protocol Performance Comparison")
        st.dataframe(
            protocol_stats.style.highlight_max(axis=0),
            use_container_width=True
        )

def enhancement_mode(demo_dreams):
    st.header("⚡ Neural Enhancement Protocols")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Current Enhancement Session")
        
        # Protocol selection
        protocol_type = st.selectbox(
            "Select Enhancement Protocol",
            [
                "🌊 Alpha Relaxation (8-12 Hz)",
                "🎨 Theta Creativity (4-8 Hz)", 
                "💾 Gamma Memory Consolidation (30-100 Hz)",
                "😴 Delta Deep Sleep (1-4 Hz)",
                "✨ Lucid Dream Induction (Mixed)"
            ]
        )
        
        # Protocol parameters
        st.subheader("⚙️ Protocol Parameters")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            frequency = st.slider("Target Frequency (Hz)", 1, 100, 10)
        with col_b:
            amplitude = st.slider("Stimulation Amplitude", 0.1, 1.0, 0.3)
        with col_c:
            duration = st.slider("Session Duration (min)", 5, 60, 20)
        
        # Enhancement visualization
        if st.button("🚀 Start Enhancement Session", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate enhancement session
            for i in range(101):
                progress_bar.progress(i)
                if i < 20:
                    status_text.text(f"🧠 Initializing neural interface... {i}%")
                elif i < 40:
                    status_text.text(f"⚡ Calibrating stimulation parameters... {i}%")
                elif i < 80:
                    status_text.text(f"🌊 Delivering targeted stimulation... {i}%")
                else:
                    status_text.text(f"✅ Completing session and monitoring... {i}%")
                
                time.sleep(0.05)
            
            st.success("🎉 Enhancement session completed successfully!")
            
            # Show session results
            st.markdown("""
            <div class="dream-card">
                <h4>📊 Session Results</h4>
                <p><strong>Protocol:</strong> Alpha Relaxation</p>
                <p><strong>Effectiveness:</strong> 87% (Excellent)</p>
                <p><strong>Neural Response:</strong> Strong alpha wave entrainment detected</p>
                <p><strong>Predicted Enhancement:</strong> Improved relaxation and dream recall</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhancement waveform visualization
        st.subheader("🌊 Stimulation Waveform Preview")
        
        t = np.linspace(0, 2, 1000)  # 2 second preview
        stimulation_wave = amplitude * np.sin(2 * np.pi * frequency * t)
        
        fig_stim = go.Figure()
        fig_stim.add_trace(go.Scatter(
            x=t,
            y=stimulation_wave,
            mode='lines',
            name='Stimulation Signal',
            line=dict(color='#f72585', width=3)
        ))
        
        fig_stim.update_layout(
            title=f"Neural Stimulation Preview - {frequency} Hz",
            xaxis_title="Time (seconds)",
            yaxis_title="Amplitude",
            height=300
        )
        st.plotly_chart(fig_stim, use_container_width=True)
    
    with col2:
        st.subheader("📋 Protocol Library")
        
        protocols = [
            {
                "name": "🌊 Alpha Relaxation",
                "frequency": "8-12 Hz",
                "purpose": "Reduce anxiety, improve dream recall",
                "effectiveness": "89%"
            },
            {
                "name": "🎨 Theta Creativity", 
                "frequency": "4-8 Hz",
                "purpose": "Enhance creative problem-solving",
                "effectiveness": "84%"
            },
            {
                "name": "💾 Gamma Memory",
                "frequency": "30-100 Hz", 
                "purpose": "Strengthen memory consolidation",
                "effectiveness": "92%"
            },
            {
                "name": "😴 Delta Deep Sleep",
                "frequency": "1-4 Hz",
                "purpose": "Improve sleep quality and recovery",
                "effectiveness": "95%"
            },
            {
                "name": "✨ Lucid Induction",
                "frequency": "Mixed",
                "purpose": "Increase lucid dreaming frequency",
                "effectiveness": "76%"
            }
        ]
        
        for protocol in protocols:
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #667eea;">
                <h5>{protocol['name']}</h5>
                <p><strong>Frequency:</strong> {protocol['frequency']}</p>
                <p><strong>Purpose:</strong> {protocol['purpose']}</p>
                <p><strong>Effectiveness:</strong> {protocol['effectiveness']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.subheader("🏆 Your Enhancement Stats")
        st.metric("Sessions Completed", "24", "↑ 3")
        st.metric("Average Effectiveness", "88%", "↑ 5%")
        st.metric("Favorite Protocol", "Alpha Relaxation", "Used 8 times")
    
    # Safety and ethical considerations
    st.subheader("⚠️ Safety & Ethics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🛡️ Safety Measures:**
        - Real-time neural monitoring
        - Automatic safety shutoffs
        - FDA-approved stimulation levels
        - Personalized parameter limits
        - Emergency stop protocols
        """)
    
    with col2:
        st.markdown("""
        **🤝 Ethical Guidelines:**
        - Informed consent required
        - Data privacy protection
        - Right to discontinue anytime
        - No coercive applications
        - Regular ethics review
        """)

def about_mode():
    st.header("ℹ️ About Neural Dream Workshop")
    
    st.markdown("""
    <div class="main-header">
        <h2 style="color: white; text-align: center;">🧠 Neural Dream Workshop (NDW)</h2>
        <p style="color: white; text-align: center; font-size: 1.1em;">
            Advanced AI-Powered Dream Analysis & Enhancement System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Technical Overview
    st.subheader("🔬 Technical Architecture")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🧠 BCI Integration:**
        - Neuralink neural interface
        - 64-channel EEG monitoring
        - Real-time signal processing
        - Sleep stage detection
        - Dream content extraction
        
        **🤖 AI Components:**
        - Large Language Models (LLaVA)
        - RAG knowledge retrieval
        - Multimodal processing
        - CLIP embeddings
        - FAISS vector search
        """)
    
    with col2:
        st.markdown("""
        **📊 Data Processing:**
        - Neural signal analysis
        - Frequency domain decomposition
        - Symbol extraction algorithms
        - Emotion classification
        - Pattern recognition
        
        **⚡ Enhancement Systems:**
        - Closed-loop feedback
        - Targeted neural stimulation
        - Protocol optimization
        - Safety monitoring
        - Efficacy tracking
        """)
    
    # Applications
    st.subheader("🎯 Applications & Benefits")
    
    tab1, tab2, tab3 = st.tabs(["🏥 Medical", "🎨 Creative", "🧘 Wellness"])
    
    with tab1:
        st.markdown("""
        **Medical Applications:**
        
        🧠 **PTSD Treatment:**
        - Process traumatic memories safely
        - Reduce nightmare frequency
        - Improve sleep quality
        - Monitor recovery progress
        
        😴 **Sleep Disorders:**
        - Diagnose sleep patterns
        - Enhance REM sleep
        - Treat insomnia
        - Optimize sleep architecture
        
        🧘 **Mental Health:**
        - Depression symptom monitoring
        - Anxiety pattern recognition
        - Therapeutic dream guidance
        - Emotional processing support
        """)
    
    with tab2:
        st.markdown("""
        **Creative Enhancement:**
        
        🎨 **Artistic Inspiration:**
        - Capture dream imagery
        - Generate creative content
        - Explore subconscious themes
        - Enhance artistic vision
        
        💡 **Problem Solving:**
        - Incubate creative solutions
        - Access unconscious insights
        - Enhance cognitive flexibility
        - Boost innovation capacity
        
        📝 **Content Creation:**
        - Story generation
        - Character development
        - World building
        - Narrative inspiration
        """)
    
    with tab3:
        st.markdown("""
        **Wellness & Personal Growth:**
        
        🌱 **Self-Discovery:**
        - Understand subconscious patterns
        - Identify personal symbols
        - Explore inner landscape
        - Gain psychological insights
        
        😌 **Stress Management:**
        - Process daily stress
        - Emotional regulation
        - Relaxation enhancement
        - Mindfulness development
        
        🎯 **Goal Achievement:**
        - Visualize success scenarios
        - Overcome mental barriers
        - Enhance motivation
        - Practice skills in dreams
        """)
    
    # Ethical Considerations
    st.subheader("🤝 Ethical Framework")
    
    st.markdown("""
    <div class="insight-box">
        <h4>🛡️ Privacy & Security</h4>
        <p>All neural data is encrypted and stored locally. Users maintain complete control over their data with options to delete or export at any time. No dream content is shared without explicit consent.</p>
    </div>
    
    <div class="insight-box">
        <h4>⚖️ Autonomy & Consent</h4>
        <p>All enhancement protocols require informed consent. Users can opt out of any procedure at any time. The system respects individual boundaries and preferences.</p>
    </div>
    
    <div class="insight-box">
        <h4>🎯 Beneficence & Non-Maleficence</h4>
        <p>All applications focus on user benefit and well-being. Strict safety protocols prevent harm. Regular ethics reviews ensure responsible development.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Future Roadmap
    st.subheader("🚀 Future Development")
    
    roadmap_data = {
        "Phase": ["Phase 1", "Phase 2", "Phase 3", "Phase 4"],
        "Timeline": ["2024 Q4", "2025 Q1", "2025 Q2", "2025 Q4"],
        "Features": [
            "Basic dream capture & analysis",
            "Enhancement protocols & feedback", 
            "Multi-user studies & optimization",
            "Clinical trials & FDA approval"
        ],
        "Status": ["✅ Complete", "🔄 In Progress", "📋 Planned", "🔮 Future"]
    }
    
    roadmap_df = pd.DataFrame(roadmap_data)
    st.dataframe(roadmap_df, use_container_width=True)
    
    # Technical Specifications
    st.subheader("⚙️ Technical Specifications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🔧 Hardware Requirements:**
        - Neuralink N1 chip
        - 64-channel recording
        - 1000 Hz sampling rate
        - Wireless data transmission
        - Battery life: 24+ hours
        """)
    
    with col2:
        st.markdown("""
        **💻 Software Stack:**
        - Python 3.9+
        - PyTorch/TensorFlow
        - Hugging Face Transformers
        - FAISS vector database
        - Streamlit frontend
        """)
    
    with col3:
        st.markdown("""
        **☁️ Infrastructure:**
        - Edge computing capable
        - Cloud backup optional
        - Real-time processing
        - HIPAA compliant
        - 99.9% uptime SLA
        """)
    
    # Contact and References
    st.subheader("📚 References & Contact")
    
    st.markdown("""
    **Key Research Papers:**
    - "Neural Decoding of Visual Dreams" - Nature Neuroscience (2023)
    - "Closed-Loop Neural Enhancement" - Science Translational Medicine (2024)  
    - "AI-Powered Dream Interpretation" - Journal of Cognitive Enhancement (2024)
    

    **Contact Information:**
    - Email: lakshmisravya.vedantham@gmail.com
    - GitHub: github.com/ndw-project
    """)

# Run the main app
if __name__ == "__main__":
    main()